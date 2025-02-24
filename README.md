# Web-Crawling-in-Python

This project implements a recursive web crawler in Python that supports both CLI and GUI interfaces using Tkinter. It authenticates users via hardcoded credentials, crawls a given URL to a specified depth, and extracts JavaScript file references from webpages while avoiding blocked domains. The crawler leverages the Requests library for fetching content and BeautifulSoup for HTML parsing, and logs detailed output to both a GUI widget and a log file, making it a versatile tool for web data extraction and learning purposes.

# Authentication

This tool uses a hardcoded user authentication system. Modify USER_CREDENTIALS in web_crawling.py to add new users.

# Default Credentials:
1. Username: admin
2. Password: password123

# Installation Guid

# Prerequisites
Ensure you have Python installed (Python 3.8+ recommended). You can install the required dependencies using:

1. Clone the repository:
`git clone https://github.com/rahul10sah/Web-Crawling-in-Python.git`
2. Install the required Python packages:
`pip install -r requirements.txt`

# Run in GUI Mode
To launch the graphical interface:
`python web_crawling.py`

# Run in CLI Mode
To run the crawler in the command-line interface:
`python web_crawling.py cli`
