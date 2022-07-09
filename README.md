[![License GPL-3.0](https://img.shields.io/github/license/Stelvey/LICCHART)](LICENSE)

# **LICCHART**

<img src="https://raw.githubusercontent.com/Stelvey/LICCHART/main/favicon.ico" width="125">

A CLI tool to make [Last.fm](https://www.last.fm/) bar chart race animations

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

Install/update LICCHART:
```
pip install --upgrade licchart
```

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

Install/update LICCHART:
```
pip install --upgrade licchart
```

### **Windows**

Install [Python](https://www.python.org/downloads/):
* Make sure to tick a box "Add Python to PATH"

Install [ffmpeg](https://www.ffmpeg.org/download.html):
* Download [latest build](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z)
* Unzip a folder you find inside to your `C:\` drive and rename the extracted folder to `ffmpeg`
* Make sure that your path to `ffmpeg.exe` is ``C:\ffmpeg\bin\ffmpeg.exe``
* Run [cmd](https://en.wikipedia.org/wiki/Cmd.exe) as administrator
* Run the following command: `setx /m PATH "C:\ffmpeg\bin;%PATH%"`

Install [Visual C++ with Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/):
* Download [latest installer](https://aka.ms/vs/17/release/vs_BuildTools.exe) and run it
* Make sure to tick a box "Desktop development with C++" and install
* Restart your PC

Install/update LICCHART:
```
pip install --upgrade licchart
```

*Chances are you can delete Visual C++ / Build Tools after LICCHART was succesfully installed. It hasn't been tested, though. If it doesn't bother you, I suggest leaving it installed*

## **Setting API key**

In order to fetch scrobbles from Last.fm, you need to [create a Last.fm API key](https://www.last.fm/api/account/create)

You can specify what API key LICCHART should use with:
```
licchart --api KEY
```
Your key file will be stored in a current directory!

# **Usage**

Using LICCHART is straightforward, just pass in your [Last.fm](https://www.last.fm/) username! LICCHART will generate a chart with default settings for you
```
licchart USERNAME
```
Once it's complete, you will see your generated video and CSV in a current directory

CSV file reduces time of your next data fetch

You can make a better chart by customizing it to your liking

## **Customization**

You can add arguments to your command to customize your chart generation, for example:
```
licchart USERNAME -d -s 06/30/2022 -e July 1st 2022 --bars 10 --fps 60 -l 3.5
```
Command above generates a chart that:
* Processes each day (`-d`)
* Shows scrobbles from 06/30/22 til 07/01/22 (`-s 06/30/2022 -e July 1st`)
* Has 10 artists max (`--bars 10`)
* Has 60 FPS (`--fps 60`)
* Lasts 3.5 minutes (`-l 3`)

### **List of all optional arguments**
| Option  | Description | Value type | Default |
| ------------- | ------------- | ------------- | ------------- |
| -h, --help  | Shows help message in terminal and exits  | None | None |
| -v, --version  | Prints out current version and exits  | None | None |
| -a *KEY*, --api *KEY*  | Changes API key and exits  | String | None |
| -m, --months  |  Takes less time to generate, but gives a less accurate result | None | Yes |
| -d, --days  | Takes quite a while to generate, but gives a very accurate result  | None | No |
| -s *DATE*, --start *DATE* | Sets starting date (month goes first) | Date String | Your first scrobble |
| -e *DATE*, --end *DATE* | Sets ending date (month goes first) | Date String | Your last scrobble |
| -b *AMOUNT*, --bars *AMOUNT* | Sets how many artists will be visible on the chart | Integer | 20 |
| -l *MIN*, --length *MIN* | Sets how long your animation will be | Decimal | Dynamic value |
| -f *FPS*, --fps *FPS* | More frames take more time to generate, but provide a smoother animation | Integer | 30 |

# **Uninstalling**

Uninstall LICCHART
```
pip uninstall licchart
```

Uninstall dependencies with package manager you used to install them

# **Troubleshooting**

In rare cases you might get an error while installing LICCHART on Windows. To troubleshoot this:
* Open [Build Tools installer](https://aka.ms/vs/17/release/vs_BuildTools.exe) again
* Uninstall Visual Studio Build Tools
* Find Visual Studio Community in "Available" tab
* Select Python and C++ options and install it