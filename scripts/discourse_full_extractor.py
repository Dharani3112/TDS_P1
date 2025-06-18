#!/usr/bin/env python3
"""
TDS Discourse Category Scraper
==============================
Scrapes topics from the TDS Knowledge Base category within a specific date range,
and also ensures that any specific topics required by the test suite are fetched.
"""

import re
import json
import requests
from datetime import datetime, timezone
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


# Date range from project spec
START_DATE = datetime(2025, 1, 1, tzinfo=timezone.utc)
END_DATE = datetime(2025, 4, 14, 23, 59, 59, tzinfo=timezone.utc)

# Paths
BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)
TEST_FILE_PATH = BASE_DIR.parent / "test_virtual_ta_api.py"


# TDS Knowledge Base category URL
TDS_CATEGORY_URL = "https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34"


def extract_topic_ids_from_test_file(test_file: Path) -> set[int]:
    """Parses the test file to find all mentioned discourse topic IDs."""
    if not test_file.exists():
        print(f"⚠️ Test file not found at {test_file}, skipping ID extraction.")
        return set()

    print(f"🔍 Reading test file to find required topic IDs: {test_file.name}")
    content = test_file.read_text(encoding="utf-8")
    
    # Regex to find all discourse topic URLs and extract their IDs
    found_ids = re.findall(r'https://discourse\.onlinedegree\.iitm\.ac\.in/t/[^/]+/(\d+)', content)
    
    if not found_ids:
        print("🤷 No topic IDs found in the test file.")
        return set()
        
    topic_ids = {int(id) for id in found_ids}
    print(f"✅ Found {len(topic_ids)} required topic IDs from tests: {topic_ids}")
    return topic_ids


def launch_chrome_and_login():
    """Launch Chrome browser and navigate to TDS category for manual login."""
    opts = Options()
    opts.add_argument("--start-maximized")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    
    # Fix chromedriver path issue
    try:
        driver_path = ChromeDriverManager().install()
    except Exception as e:
        print(f"❌ Could not download chromedriver: {e}")
        return None

    if driver_path and driver_path.endswith("THIRD_PARTY_NOTICES.chromedriver"):
        driver_path = driver_path.replace("THIRD_PARTY_NOTICES.chromedriver", "chromedriver.exe")
    
    try:
        service = ChromeService(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=opts)
    except Exception as e:
        print(f"❌ Failed to launch Chrome: {e}")
        return None

    driver.get(TDS_CATEGORY_URL)
    print("Please complete the login in the opened browser window.")
    print("Press Enter here once you're logged in and can see the TDS category page.")
    input()
    return driver


def create_authenticated_session(driver):
    """Extract cookies from Selenium driver to create authenticated requests session."""
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    })
    
    for cookie in driver.get_cookies():
        session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])
    
    return session


def is_within_date_range(timestamp_str: str) -> bool:
    """Check if timestamp is within our target date range."""
    try:
        post_date = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        return START_DATE <= post_date <= END_DATE
    except (ValueError, TypeError):
        return False


def scrape_topic_ids_from_category(session):
    """Scrape topic IDs from TDS category pages based on creation or last post date."""
    topic_ids = set()
    page = 0
    
    print(f"Scraping TDS topics from {START_DATE.date()} to {END_DATE.date()}...")
    
    while True:
        url = f"{TDS_CATEGORY_URL}.json?page={page}"
        response = session.get(url)
        if response.status_code != 200:
            break
        
        data = response.json()
        topic_list = data.get("topic_list", {}).get("topics", [])
        
        if not topic_list:
            break
            
        for topic in topic_list:
            if is_within_date_range(topic['created_at']) or is_within_date_range(topic['last_posted_at']):
                topic_ids.add(topic['id'])
        
        page += 1
    
    print(f"Found {len(topic_ids)} topics in date range from category scan.")
    return list(topic_ids)


def download_topic_details(session, topic_ids):
    """Download full JSON for each topic."""
    topic_summaries = []
    
    print(f"Downloading details for {len(topic_ids)} topics...")
    
    for i, topic_id in enumerate(sorted(list(topic_ids)), 1):
        file_path = RAW_DIR / f"topic-{topic_id}.json"
        if file_path.exists():
            print(f"  ({i}/{len(topic_ids)}) Skipping topic {topic_id}, already exists.")
            continue

        print(f"  ({i}/{len(topic_ids)}) Downloading topic {topic_id}...")
        url = f"https://discourse.onlinedegree.iitm.ac.in/t/{topic_id}.json"
        response = session.get(url)
        
        if response.status_code == 200:
            data = response.json()
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            
            summary = {
                "id": data.get("id"),
                "title": data.get("title"),
                "created_at": data.get("created_at"),
                "posts_count": data.get("posts_count"),
            }
            topic_summaries.append(summary)
        else:
            print(f"  ❌ Failed to download topic {topic_id}, status: {response.status_code}")
    
    # Save summary file
    summary_path = RAW_DIR / "_scraped_topic_summaries.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(topic_summaries, f, indent=2)
    print(f"✅ Saved summary of {len(topic_summaries)} newly downloaded topics to {summary_path.name}")


def main():
    """Main execution flow."""
    print("🚀 Starting TDS Discourse Scraper...")
    
    required_ids = extract_topic_ids_from_test_file(TEST_FILE_PATH)
    
    driver = launch_chrome_and_login()
    if not driver:
        return
        
    session = create_authenticated_session(driver)
    driver.quit()
    
    scraped_ids = scrape_topic_ids_from_category(session)
    
    all_topic_ids = required_ids.union(scraped_ids)
    
    if not all_topic_ids:
        print("🤷 No topics to download. Exiting.")
        return
        
    download_topic_details(session, all_topic_ids)
    
    print("✅ Scraping complete.")


if __name__ == "__main__":
    main()