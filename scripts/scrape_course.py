#!/usr/bin/env python3
"""
Script to scrape TDS course content.
This script scrapes the main TDS course website for educational content.
"""

import sys
import os
import asyncio
from datetime import datetime

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.scraper import WebScraper
from app.core.config import settings
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('course_scraping.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Main function to scrape course content."""
    logger.info("Starting TDS course content scraping...")
    
    try:
        # Initialize scraper
        scraper = WebScraper()
        
        # Scrape course content
        logger.info(f"Scraping content from: {settings.course_url}")
        course_data = scraper.scrape_course_content()
        
        if course_data:
            # Save the scraped data
            scraper.save_scraped_data(course_data, "course_content.json")
            logger.info(f"Successfully scraped {len(course_data)} course pages")
            
            # Print summary
            print(f"\n=== Scraping Summary ===")
            print(f"Total pages scraped: {len(course_data)}")
            print(f"Data saved to: app/data/knowledge_base/course_content.json")
            print(f"Scraping completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Show sample of scraped content
            print(f"\n=== Sample Content ===")
            for i, item in enumerate(course_data[:3]):
                print(f"{i+1}. {item['title']}")
                print(f"   URL: {item['url']}")
                print(f"   Content preview: {item['content'][:150]}...")
                print()
        else:
            logger.warning("No content was scraped")
            
    except Exception as e:
        logger.error(f"Error during scraping: {e}")
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
