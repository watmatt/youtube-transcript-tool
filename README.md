# YouTube Transcript Tool

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

A simple desktop tool for downloading YouTube video transcripts with an intuitive interface. Just paste a YouTube URL and get the transcript automatically saved with the video title.

## ✨ Features

- 🖥️ **Simple popup interface** - No complex setup needed
- 🔗 **URL input with validation** - Paste any YouTube URL format
- 📦 **Auto-installs dependencies** - No manual package installation required
- 📁 **Smart file naming** - Saves transcripts with clean video titles
- 🌐 **Cross-platform** - Works on Windows, Mac, and Linux
- 🖥️ **GUI & CLI versions** - Choose your preferred interface

## 🚀 Quick Start

### Windows
1. **Double-click `scripts/run_transcript_tool.bat`**
2. Enter YouTube URL in the popup
3. Transcript saved to `Transcriptions/` folder

### Linux/Mac
1. **Run the install script:** `./scripts/install.sh`
2. **Run the tool:** `./scripts/run_transcript_tool.sh` or `python3 transcript_tool.py`
3. Enter YouTube URL in the popup
4. Transcript saved to `Transcriptions/` folder

### Command Line (Headless Systems)
For servers or if you prefer command line:
```bash
python3 scripts/transcript_tool_cli.py
```

## 📖 How to Use
1. **Get a YouTube URL** - Copy any YouTube video URL
2. **Run the tool** - Use the launcher or run the Python script
3. **Enter URL** - Paste the URL in the dialog
4. **Wait for download** - The tool fetches and saves the transcript
5. **Find your file** - Check the `Transcriptions/` folder

## 📋 Requirements
- **Python 3.6+** 
- **Internet connection**
- **GUI support** (for popup interface) or use CLI version for headless systems

### Linux Dependencies
- **Ubuntu/Debian:** `sudo apt-get install python3-tkinter`
- **RHEL/CentOS:** `sudo yum install tkinter` 
- **Fedora:** `sudo dnf install python3-tkinter`
- **Arch:** `sudo pacman -S tk`
- **Alternative:** Use `scripts/transcript_tool_cli.py` for command-line interface

## 📁 Project Structure
```
├── scripts/                    # 📁 All executable files
│   ├── transcript_tool.py      # 🖥️ Main GUI version with popup interface
│   ├── transcript_tool_cli.py  # 💻 Command-line version (no GUI required)
│   ├── run_transcript_tool.bat # 🪟 Windows launcher
│   ├── run_transcript_tool.sh  # 🐧 Linux/Mac launcher  
│   ├── install.bat             # 🪟 Windows installation script
│   └── install.sh              # 🐧 Linux/Mac installation script
├── requirements.txt            # 📦 Python dependencies
├── Transcriptions/             # 📂 Output folder for transcript files
├── .github/                    # 📁 GitHub-specific files
│   ├── CONTRIBUTING.md         # 🤝 Contribution guidelines
│   └── ISSUE_TEMPLATE/         # 📋 Issue templates
├── LICENSE                     # ⚖️ MIT License
└── README.md                   # 📖 This file
```

## 🔧 Dependencies (Auto-installed)
- `youtube-transcript-api` - For fetching YouTube transcripts
- `requests` - For web requests
- `beautifulsoup4` - For parsing video titles
- `tkinter` - For popup interface (included with Python)

## 📝 Notes
- ✅ Transcripts are only available for videos that have captions/subtitles
- ✅ Handles most YouTube URL formats automatically
- ✅ Files are saved in UTF-8 encoding for international characters
- ✅ Video titles are sanitized to be filesystem-safe
- ⚠️ Some videos may have restricted or no available transcripts

## 🤝 Contributing
We welcome contributions! Please see our [Contributing Guidelines](.github/CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author
**Watmatt** - [GitHub](https://github.com/watmatt)
