[![License GPL-3.0](https://img.shields.io/github/license/Stelvey/LICCHART)](LICENSE)

# **LICCHART**

<img src="https://raw.githubusercontent.com/Stelvey/LICCHART/main/favicon.ico" width="125">

A CLI tool to make [Last.fm](https://www.last.fm/) bar chart race animations

<br>

# **Installation**

### **Linux**

Make sure you have [Python](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/installation/) (use your own package manager!):
```
sudo apt-get install python3
```

Install [ffmpeg](https://www.ffmpeg.org/download.html):
```
sudo apt-get install ffmpeg
```

Install/update [LICCHART](https://github.com/Stelvey/LICCHART):
```
pip install --upgrade licchart
```

<br>

### **macOS**

Install [Homebrew](https://brew.sh/) package manager:
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Make sure you have [Python](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/installation/):
```
brew install python 
```

Install [ffmpeg](https://www.ffmpeg.org/download.html):
```
brew install ffmpeg
```

Install/update [LICCHART](https://github.com/Stelvey/LICCHART):
```
pip install --upgrade licchart
```

<br>

### **Windows**

Install [Python](https://www.python.org/downloads/):
* Make sure to tick a box "Add Python to PATH"

Install [ffmpeg](https://www.ffmpeg.org/download.html):
* Download [latest build](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z)
* Unzip all files inside the folder `C:\ffmpeg`
* Run cmd as administrator
* Run the following command: `setx /m PATH "C:\ffmpeg\bin;%PATH%"`
* You might need to restart your PC afterwards

Install/update [LICCHART](https://github.com/Stelvey/LICCHART):
```
pip install --upgrade licchart
```

<br>

## **Setting API key**

In order to fetch scrobbles from Last.fm, you need to [create a Last.fm API key](https://www.last.fm/api/account/create)

You can specify what API key [LICCHART](https://github.com/Stelvey/LICCHART) should use with:
```
licchart --api KEY
```

<br>

## **Uninstalling**



<br>

# **Usage**

Using [LICCHART](https://github.com/Stelvey/LICCHART) is straightforward, just pass in your [Last.fm](https://www.last.fm/) username!
```
licchart USERNAME
```
Once it's complete, you will see your generated video and CSV in a current directory

CSV file reduces time of your next data fetch

<br>

## **Customization**

You can add arguments to your command to customize your chart generation
```
licchart -d -s 06/30/2022 -e July 1st 2022 --bars 10 --fps 60 -l 3.5
```
Command above generates a chart that:
* Processes each day (`-d`)
* Shows scrobbles from 06/30/22 til 07/01/22 (`-s 06/30/2022 -e July 1st`)
* Has 10 artists max (`--bars 10`)
* Has 60 FPS (`--fps 60`)
* Lasts 3.5 minutes (`-l 3`)

<br>

### **List of all arguments**
| Option  | Description | Value type | Default |
| ------------- | ------------- | ------------- | ------------- |
| -h, --help  | Shows help message in terminal and exits  | None | None |
| -v, --version  | Prints out current version and exits  | None | None |
| -a *KEY*, --api *KEY*  | Changes API key and exits  | String | None |
| -m, --months  |  Takes less time to generate, but gives a less accurate result | None | Yes |
| -d, --days  | Takes quite a while to generate, but gives very accurate result  | None | No |
| -s *DATE*, --strt *DATE* | Sets starting date | Date String | Your first scrobble |
| -e *DATE*, --end *DATE* | Sets ending date | Date String | Your last scrobble |
| -b *AMOUNT*, --bars *AMOUNT* | Sets how many artists will be visible on the chart | Integer | 20 |
| -l *MIN*, --length *MIN* | Sets how long your animation will be | Decimal | Dynamic value |
| -f *FPS*, --fps *FPS* | More frames take more time to generate, but provide a smoother animation | Integer | 30 |