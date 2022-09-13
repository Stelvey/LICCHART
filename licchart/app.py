import csv
from matplotlib import pyplot as plt
import bar_chart_race as bcr
import argparse
import sys
from licchart.helpers import catcher, dataperiod, datatodf, fetch, internetcheck, update, getjson, apichecker
import dateutil.parser
import regex as re

def licchart():
    parser = argparse.ArgumentParser(description='A Last.fm Bar Chart Race Maker.', epilog='Visit https://github.com/Stelvey/LICCHART/ for more info.')
    parser.add_argument('-v', '--version', help='print out current version and exit', action='version', version='LICCHART 0.1.4')

    parser.add_argument('source', help='str: your last.fm username or csv filename', nargs='?')

    parser.add_argument('-a', '--api', help='str: add/change custom api key and exit', metavar='KEY')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-m', '--months', help='takes less time to generate, but gives a less accurate result (default)', action='store_true')
    group.add_argument('-d', '--days', help='takes quite a while to generate, but gives very accurate result', action='store_true')

    parser.add_argument('-s', '--start', help='str (month first): set starting date (default: your first scrobble)', metavar='DATE')
    parser.add_argument('-e', '--end', help='str (month first): set ending date (default: your last scrobble)', metavar='DATE')

    parser.add_argument('-b', '--bars', type=int, default=20, help='int: set how many artists will be visible on the chart (default: %(default)s)', metavar='AMT')
    parser.add_argument('-l', '--length', type=float, help='float: set how long your animation will be (default: dynamic value)', metavar='MIN')
    parser.add_argument('-f', '--fps', type=int, default=30, help='int: more frames take more time to generate, but provide a smoother animation (default: %(default)s)', metavar='FPS')

    args = parser.parse_args()

    # Check internet
    if internetcheck():
        sys.exit(catcher(internetcheck()))

    # Some default chart values
    type = 'months'
    length = None

    # API input
    if args.api:
        rawjson = getjson({'api_key': args.api})
        if apichecker(rawjson) == 6:
            sys.exit(catcher(5))
        with open('api.key', 'w', encoding="utf-8") as f:
            f.write(args.api)
        return print('API key changed successfully')
    try:
        with open('api.key', 'r', encoding="utf-8") as f:
            api = f.read()
    except FileNotFoundError:
        print("You haven't set an API key!\nYou can get one at: https://www.last.fm/api/account/create\nPlease, enter it now:")
        api = input()
        if len(api) > 16:
            with open('api.key', 'w', encoding="utf-8") as f:
                f.write(api)
        else:
            sys.exit(catcher(5))

    # Type input
    if args.days:
        type = 'days'

    # Range inputs
    if args.start:
        try:
            start = dateutil.parser.parse(args.start).date()
        except ValueError:
            sys.exit(catcher(3))
    else:
        start = None
    if args.end:
        try:
            end = dateutil.parser.parse(args.end).date()
        except ValueError:
            sys.exit(catcher(3))
        if start > end:
            sys.exit(catcher(1))
    else:
        end = None

    # Bars, length, smooth inputs
    try:
        bars = int(args.bars)
    except ValueError:
        sys.exit(catcher(3))
    if bars < 1:
        sys.exit(catcher(3))

    if args.length:
        try:
            length = round(float(args.length), 2)
        except ValueError:
            sys.exit(catcher(3))
        if length < 0.1:
            sys.exit(catcher(3))

    try:
        smooth = int(args.fps) / 1000
    except ValueError:
        sys.exit(catcher(3))
    if smooth < 0.01:
        sys.exit(catcher(3))

    # Source input
    if args.source == None:
        print("You haven't specified your source (nickname or CSV filename).\nPlease, enter it now:")
        args.source = input()
        if not args.source:
            sys.exit(catcher(0))

    # Making a source var + support for " and '
    source = args.source.replace('[\"\'](.*)[\"\']', '')

    # This abomination finds CSV or uses username instead (to create/update data)
    try:
        file = open('LICCHART_' + source, 'r', encoding="utf-8")
    except FileNotFoundError:
        try:
            file = open('LICCHART_' + source + '.csv', 'r', encoding="utf-8")
        except FileNotFoundError:
            user = source
            data = fetch(user, api, 1, None)
        else:
            data = update(file, api)
            user = data[0][0].split('#', 1)[1]
    else:
        data = update(file, api)
        user = data[0][0].split('#', 1)[1]
    finally:
        if catcher(data) != None:
            sys.exit(catcher(data))

    # Making CSV file
    with open('LICCHART_' + user + '.csv', 'w', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(data)

    # Delete all scrobbles not in period range
    data = dataperiod(data, start, end)

    # Make DataFrame out of data list
    df = datatodf(data, type)
    if catcher(df) != None:
        sys.exit(catcher(df))

    # Update some default values
    if length:
        length = round(length * 60000 / len(df))
    else:
        if type == 'months':
            length = 1000
        else:
            length = 100
        
    smooth = round(smooth * length)
    print()
    print('         Periods: ' + str(len(df)))
    print('     Step length: ' + str(length))
    print('Steps per period: ' + str(smooth))
    print()
    print('Your animation is generating. It takes quite a while. Please, wait...')
    # Prepare a figure!
    fig, ax = plt.subplots(figsize = (7, 3.9), dpi = 144)
    # Chart background
    ax.set_facecolor('#1a0933')
    ax.tick_params(labelsize = 8, length = 0)
    # Set grid
    ax.grid(True, axis = 'x', color = '#32fbe2')
    # And make it below everything
    ax.set_axisbelow(True)
    # Remove black borders around chart
    [spine.set_visible(False) for spine in ax.spines.values()]
    # Video background
    fig.patch.set_facecolor('#1a0933')
    # Adjust width (fixes empty spaces)
    fig.subplots_adjust(left = 0.2, right = 0.95)
    # Set artists color
    ax.tick_params(colors='white', which='both')

    # Generate a chart!!!
    bcr.bar_chart_race(
        df = df,
        filename = 'LICCHART_' + user + '.mp4',
        fig = fig,
        shared_fontdict = {'color': 'white'},
        n_bars = bars,
        bar_label_size = 4,
        tick_label_size = 8,
        filter_column_colors = True,
        period_length = length,
        steps_per_period = smooth
    )

    print()
    print('#######################################################')
    print('#                                                     #')
    print('# Hey, check your folder. Your animation is complete! #')
    print('#                                                     #')
    print('#######################################################')
    print()