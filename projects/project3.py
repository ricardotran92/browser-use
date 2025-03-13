import csv
import time
import os
import random
from browser_use import Agent
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext

# Config
INPUT_FILE = "links.csv"
OUTPUT_FILE = "comments.csv"
LOG_FILE = "scrape_log.txt"
MAX_COMMENT = 150
RETRY_LIMIT = 3
BATCH_SIZE = 50
SCROLL_INTERVAL = 3
BROWSER_PATH = "D:\\chrome-win64\\chrome.exe"
# BROWSER_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

# Initialize browser
config=BrowserConfig(
    chrome_instance_path=BROWSER_PATH,
    headless=False
)
browser = Browser(config=config)

def read_links():
    """Đọc danh sách link từ file CSV và bỏ qua các link đã scrape thành công."""
    if not os.path.exists(INPUT_FILE):
        print(f"File {INPUT_FILE} not found.")
        return []
    
    scraped_links = []
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None) # Skip header
            scraped_links = [row[0] for row in reader]
    
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)
        links = [row[0] for row in reader if row[0] not in scraped_links]

    return links

def log_error(link, reason):
    """Ghi lỗi vào file log."""
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{link}: {reason}\n")

def scroll_page():
    """Scroll trang để tải thêm bình luận thông qua Browse_use."""
    try:
        browser.
        time.sleep(SCROLL_INTERVAL)

