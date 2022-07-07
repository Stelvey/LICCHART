import cutlet
import regex as re
import pandas as pd
import requests
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta


# I'm very tired and I made this catcher for custom error codes
def catcher(code):
    codes = {
        0: "User not found",
        1: "Current range has no data",
        2: "This is not a correct data file",
        3: "Unsupported values",
        4: "API doesn't respond",
        5: "Invalid API key!\nPlease, set a valid API key with: --api\nYou can get one at: https://www.last.fm/api/account/create",
        6: "Connection failed :("
    }
    try:
        if code in codes:
            return 'Error: ' + codes[code]
    except:
        return None


# API-related errors
def apichecker(rawjson):
    try:
        # User not found error
        if rawjson['error'] == 6:
            return 0
        # API key error
        if rawjson['error'] == 10:
            return 6
    except KeyError:
        return None


# Internet connection checker
def internetcheck():
    try:
        apichecker(getjson(None))
    except requests.exceptions.ConnectionError:
        return 6
    else:
        return None


# Cut the now playing track, return cut version (it sometimes IndexErrors for some reason)
def cutnowplaying(scrobbles):
    try:
        if scrobbles[0].get('@attr'):
            return scrobbles[1:]
        else:
            return scrobbles
    except IndexError:
        print('IndexError occured (assuming user is not playing anything?)')


# Check if the file is correct
def iscsv(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'csv'


# Get raw json from API call
def getjson(parameters):
    response = requests.get(f"https://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&format=json", params=parameters)
    return response.json()


# Return correct formatting (date or month)
def strftype(type):
    if type == 'months':
        return '%B %Y'
    elif 'days':
        return '%b %d, %Y'


# Turn timestamp into a date
def tstodate(ts):
        return datetime.fromtimestamp(int(ts), tz=timezone.utc).date()


# I have no idea what I'm doing (this is because datetime forces days)
def datecompare(date, type):
    if type == 'months':
        return [date.year, date.month]
    else:
        return [date.year, date.month, date.day]


# Prepare data list for the selected time period (not the fastest method)
def dataperiod(data, start, end):
    for scrobble in data[1:]:
        scrblts = tstodate(scrobble[0])
        if start and start > scrblts:
            data.remove(scrobble)
        if end and end < scrblts:
            data.remove(scrobble)
    return data


# Data to DF (days/months)
def datatodf(data, type):
    # Prepare dataframe, empty dict, loop iteration flag, day/month
    df = pd.DataFrame()
    dict = {}
    first = True

    # Cutlet var
    katsu = cutlet.Cutlet()

    print()
    print('Pushing scrobbles to DataFrame...')
    for scrobble in data[1:]:
        # Get current scrobble's date and artist
        scrbldate = tstodate(scrobble[0])
        # (These dollar signs were messing up the code, a temp fix?)
        scrblartist = scrobble[1].replace('$', 'S')
        # Turn "unknown glyphs" into romaji
        if re.match('[\p{Katakana}\p{Han}\p{Hiragana}\p{Bopomofo}]', scrblartist):
            scrblartist = katsu.romaji(scrblartist)
        # Get a date var the first while loop iteration
        if first:
            currentdate = scrbldate
            first = False
        
        # Check if it is time to push a day/month to dataframe
        if datecompare(currentdate, type) != datecompare(scrbldate, type):
            df = pd.concat([df, pd.DataFrame(dict, index=[currentdate.strftime(strftype(type))])])
            
            # This is for filling empty days/months (if there are any) with same data
            while datecompare(currentdate + relativedelta(**{type: 1}), type) < datecompare(scrbldate, type):
                currentdate += relativedelta(**{type: 1})
                df = pd.concat([df, pd.DataFrame(dict, index=[currentdate.strftime(strftype(type))])])

            # Update to a new date as well
            currentdate = scrbldate
        
        # Add a new artist to data or add a scrobble to an existing one
        if scrblartist in dict:
            dict[scrblartist] += 1.0
        else:
            dict[scrblartist] = 1.0

    # Push final day/month to dataframe (if any data was received)
    try:
        df = pd.concat([df, pd.DataFrame(dict, index=[currentdate.strftime(strftype(type))])])
    except UnboundLocalError:
        return 1

    # Fill in the NaN and give index a name ^^ owo
    df.fillna(0, inplace=True)
    df.index.name = 'Date'

    print('DataFrame is ready!')
    return df


# Collect all (optionally only new) scrobbles to data list!
def fetch(user, api, page, ts):
    # Set parameters for API call
    parameters = {
        'api_key': api,
        'limit': 1000,
        'user': user,
        'page': page
    }

    # Make an API call (checking it) and put JSON into a var
    rawjson = getjson(parameters)
    if apichecker(rawjson) != None:
        return apichecker(rawjson)

    # Call API again when it sometimes KeyErrors for some reason 
    success = False
    attempt = 0
    while not success:
        try:
            # Find out total pages
            pages = int(rawjson['recenttracks']['@attr']['totalPages'])
        except KeyError:
            print('KeyError occured, trying again')
            attempt += 1
            if attempt == 5:
                # API error
                return 4
            rawjson = getjson(parameters)
        else:
            success = True

    # Start with the last page (if not [UPDATING])
    if not ts:
        parameters['page'] = pages

    # Prepare data list with header
    data = [['timestamp#' + user, 'artist']]

    print()
    while True:
        # Stupidly make a 2nd API call, this time starting from the last page (and looping)
        rawjson = getjson(parameters)

        # Call API again when it sometimes KeyErrors for some reason
        success = False
        while not success:
            try:
                # Get all the scrobbles from a page
                scrobbles = rawjson['recenttracks']['track']
            except KeyError:
                print('KeyError occured, trying again')
                rawjson = getjson(parameters)
            else:
                success = True

        # Cut the now playing track
        scrobbles = cutnowplaying(scrobbles)

        for scrobble in reversed(scrobbles):
            # [UPDATING] Skip old scrobbles
            if ts and int(scrobble['date']['uts']) <= ts:
                continue
            # Fix "unknown date" scrobbles' dates
            elif int(scrobble['date']['uts']) <= 1108290000:
                scrbldate = 1108290000
            # Or just get current scrobble's date and artist
            else:
                scrbldate = scrobble['date']['uts']
            # (These dollar signs were messing up the code, a temp fix?)
            scrblartist = scrobble['artist']['#text'].replace('$', 'S')
            # Add to data list
            data += [[scrbldate, scrblartist]]
        
        # Switch to a new page
        print(f"FETCH: {pages - parameters['page'] + 1} out of {pages}")
        parameters['page'] -= 1

        if parameters['page'] < 1:
            break

    return data


# Update the CSV
def update(file, api):
    try:
        df = pd.read_csv(file)
    except:
        return 2

    # Get user
    user = df.columns[0].split('#', 1)[1]

    # Set parameters for API call
    parameters = {
        'api_key': api,
        'limit': 1000,
        'user': user,
        'page': 1
    }

    # Make an API call (checking it) and put JSON into a var
    rawjson = getjson(parameters)
    if apichecker(rawjson) != None:
        return apichecker(rawjson)

    # Call API again when it sometimes KeyErrors for some reason
    success = False
    attempt = 0
    while not success:
        try:
            # Find out total pages
            pages = int(rawjson['recenttracks']['@attr']['totalPages'])
        except KeyError:
            print('KeyError occured, trying again')
            attempt += 1
            if attempt == 5:
                return 0
            rawjson = getjson(parameters)
        else:
            success = True

    # Get latest timestamp
    ts = df.iloc[-1][0]

    # Find the page from where to start
    print()
    while True:
        # Call API again when it sometimes KeyErrors for some reason
        success = False
        while not success:
            try:
                # Get all the scrobbles from a page
                scrobbles = rawjson['recenttracks']['track']
            except KeyError:
                print('KeyError occured, trying again')
                rawjson = getjson(parameters)
            else:
                success = True

        # Cut the now playing track
        scrobbles = cutnowplaying(scrobbles)

        for scrobble in reversed(scrobbles):
            scrbldate = int(scrobble['date']['uts'])
            if scrbldate == ts:
                print('Pages collected! Starting your update')
                page = parameters['page']
                # Return old and now updated data (header + old + new w/o header)
                return [df.columns.values.tolist()] + df.values.tolist() + fetch(user, api, page, ts)[1:]
        
        # Switch to a new page
        print(f"Pages to update: {parameters['page']}")
        parameters['page'] += 1

        # In case that a user has nothing to do in life
        # And deletes that particular scrobble
        # Probably to fuck up the code
        if parameters['page'] > pages:
            return None

        # Make a new API call requesting next page
        rawjson = getjson(parameters)