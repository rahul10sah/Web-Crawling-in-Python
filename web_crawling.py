import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from urllib.parse import urljoin
import hashlib
import getpass
import logging
import sys

# Configure logging
logging.basicConfig(filename="crawler.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Hardcoded username and hashed password (for demonstration purposes)
USER_CREDENTIALS = {
    "admin": hashlib.sha256("password123".encode()).hexdigest()
}

# List of blocked domains (for security reasons)
BLOCKED_DOMAINS = ["example.com", "phishing.com"]


def authenticate():
    username = simpledialog.askstring("Login", "Enter username:")
    password = simpledialog.askstring("Login", "Enter password:", show='*')
    if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == hashlib.sha256(password.encode()).hexdigest():
        return True
    messagebox.showerror("Authentication Failed", "Invalid username or password!")
    return False


class WebCrawler:
    def __init__(self, url, max_depth, output_text_widget=None):
        self.url = url
        self.max_depth = max_depth
        self.subdomains = set()
        self.links = set()
        self.jsfiles = set()
        self.output_text = output_text_widget

    def start_crawling(self):
        self.log_output(f"\033[1m\033[36mRecursive Web Crawler starting at {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\033[0m")
        self.log_output("-" * 80)
        self.log_output(f"[*] URL             {self.url}")
        self.log_output(f"[*] Max Depth       : {self.max_depth}")
        self.log_output("-" * 80)
        self.crawl(self.url, depth=1)

    def crawl(self, url, depth):
        if depth > self.max_depth or any(blocked in url for blocked in BLOCKED_DOMAINS):
            return

        try:
            response = requests.get(url, timeout=5, allow_redirects=True)
            soup = BeautifulSoup(response.text, 'html.parser')
        except requests.exceptions.RequestException as err:
            self.log_output(f"[-] An error occurred: {err}")
            return

        for file in soup.find_all('script'):
            script_src = file.get('src')
            if script_src:
                self.jsfiles.add(script_src)
                self.log_output(f"[+] JS Files : {script_src}")

    def log_output(self, message):
        if self.output_text:
            self.output_text.insert(tk.END, message + "\n")
        logging.info(message)


class WebCrawlerCLI:
    @staticmethod
    def start():
        username = input("Enter username: ")
        password = getpass.getpass("Enter password: ")
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == hashlib.sha256(password.encode()).hexdigest():
            url = input("Enter URL: ")
            depth = int(input("Enter depth: "))
            crawler = WebCrawler(url, depth)
            crawler.start_crawling()
        else:
            print("Authentication failed! Exiting...")


class WebCrawlerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Web Crawler GUI")
        if not authenticate():
            root.destroy()
            return

        tk.Label(root, text="Enter URL:").pack(pady=5)
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.pack(pady=5)
        
        tk.Label(root, text="Enter Depth:").pack(pady=5)
        self.depth_entry = tk.Entry(root, width=50)
        self.depth_entry.pack(pady=5)
        
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Start Crawling", command=self.start_crawl).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Clear Output", command=self.clear_output).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Delete & Restart", command=self.delete_restart).pack(side=tk.LEFT, padx=5)

        self.output_text = scrolledtext.ScrolledText(root, width=80, height=20)
        self.output_text.pack(pady=5)
    
    def start_crawl(self):
        url = self.url_entry.get()
        try:
            depth = int(self.depth_entry.get())
        except ValueError:
            self.output_text.insert(tk.END, "[-] Invalid depth value.\n")
            return

        if not url:
            self.output_text.insert(tk.END, "[-] Please enter a URL.\n")
            return

        self.output_text.delete(1.0, tk.END)
        crawler = WebCrawler(url, depth, self.output_text)
        crawler.start_crawling()
    
    def clear_output(self):
        self.output_text.delete(1.0, tk.END)
    
    def delete_restart(self):
        self.clear_output()
        self.url_entry.delete(0, tk.END)
        self.depth_entry.delete(0, tk.END)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "cli":
        WebCrawlerCLI.start()
    else:
        root = tk.Tk()
        app = WebCrawlerApp(root)
        root.mainloop()
