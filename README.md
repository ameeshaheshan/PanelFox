<h1 align="center">
  <br>
  <a href="https://github.com/ameeshaheshan/PanelFox/"><img src="https://github.com/ameeshaheshan/PanelFox/blob/main/src/banner.png" alt="PanelFox"></a>
  <br>
  PanelFox 🦊
  <br>
</h1>


<div align="center">

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Version](https://img.shields.io/badge/version-2.0-blue.svg)

**PanelFox 🦊: Uncover Hidden Admin Panels 🔍, Boost Your Reconnaissance Skills 💻, and Enhance Your Security Assessments 🔐**

[Features](#✨-features) • [Installation](#🚀-installation) • [Usage](#💡-usage) • [Examples](#📚-examples) • [Contributing](#🤝-contributing)

</div>
<div align="center">
  <img src="https://github.com/ameeshaheshan/PanelFox/blob/main/src/img1.png" alt="PanelFox"></a>
  <img src="https://github.com/ameeshaheshan/PanelFox/blob/main/src/img2.png" alt="PanelFox"></a>
  <img src="https://github.com/ameeshaheshan/PanelFox/blob/main/src/img3.png" alt="PanelFox"></a>
</div>

## 🎯 Overview

PanelFox 🦊 is a Python-based admin panel finder designed for penetration testers and security researchers to efficiently locate hidden admin interfaces in web applications. Using deep URL crawling and intelligent scanning techniques, it uncovers admin login portals that are often overlooked or deliberately obscured. With features like smart filtering and efficient scanning, PanelFox quickly identifies potential vulnerabilities in web applications, making it an essential tool for enhancing reconnaissance efforts and improving overall security assessments.

## ✨ Features

- **Deep URL Crawling 🕵️‍♂️**: Thoroughly scans websites to find hidden admin panel URLs, ensuring no portal is left behind.
- **Smart Filtering 🔍**: Automatically filters admin panel links based on common naming conventions and patterns for greater accuracy.
- **Efficient Scanning ⚡**: Fast and precise scanning to save time during reconnaissance and speed up vulnerability assessments.
- **User-Friendly Interface 👨‍💻**: Simple command-line interface (CLI) for easy usage, even for beginners.
- **Background Operation 🔒**: Runs invisibly and silently, logging all user input.
- **Real-time Logging ⏱️**:  Provides live, real-time logs during the scan process, giving instant feedback and insights into the tool's progress..
- **Cross-Platform Support 💻**: Works on Windows, Linux, and macOS systems.
- **Customizable Options ⚙️**: Easily configurable to suit different testing environments and websites.
- **Open Source 🔓**: Completely open-source, allowing you to contribute, modify, or enhance the tool as needed.

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/ameeshaheshan/PanelFox.git

# Navigate to the directory
cd NebulaDork

# Install requirements
pip install -r requirements.txt

# Run script
python app.py -h
```

## 💡 Usage

```bash
usage: app.py [-h] -u URL -w WORD_LIST [-t {1,2,3,4,5,6,7,8,9,10}] [-X {GET,POST,HEAD,PUT,DELETE}]
              [-H HEADER] [--cookie COOKIE] [--delay DELAY] [--show-headers] [-l] [-v] [-p PROXY]
              [-o OUTPUT] [-I] [--user-agent USER_AGENT] [--save-responses]
              [--status-code-filter STATUS_CODE_FILTER]
```

### 🔧 Options

```bash
Hidden Admin Panel Finder Tool

options:
  -h, --help            show this help message and exit
  -u, --url URL         Target URL (e.g. http://example.com)
  -w, --word-list WORD_LIST
                        Wordlist file containing admin paths
  -t, --threads {1,2,3,4,5,6,7,8,9,10}
                        Number of threads (1-10)
  -X, --method {GET,POST,HEAD,PUT,DELETE}
                        HTTP method to use
  -H, --header HEADER   Add custom headers (e.g. 'X-API-Key: 12345')
  --cookie COOKIE       Add cookies (e.g. 'session_id=abc123; token=xyz')
  --delay DELAY         Add random delay between requests (seconds)
  --show-headers        Display response headers for found pages
  -l, --log             Enable logging of requests
  -v, --verbose         Enable verbose mode
  -p, --proxy PROXY     Proxy list file
  -o, --output OUTPUT   Save results to a file
  -I, --ignore-ssl      Ignore SSL certificate warnings
  --user-agent USER_AGENT
                        User-Agent list file
  --save-responses      Save HTTP responses for analysis
  --status-code-filter STATUS_CODE_FILTER
                        Filter results by HTTP status code
```

## 📚 Basic Usage

### Find admin panels using a simple wordlist

```bash
python app.py -u http://example.com -w {path-to-wordlist}.txt
```

This command will:
- -u http://example.com → Specifies the target URL.
- -w admin_paths.txt → Loads a wordlist of potential admin paths.

## 📚 Intermediate Usage

### Increase speed with multi-threading

```bash
python app.py -u http://example.com -w admin_paths.txt -t 5
```

This command will:
- -t 5 → Uses 5 threads to speed up the scan.
- Can use t 1 to t 10
