#!/usr/bin/env python3
"""
Script to scrape TDS Discourse forum content.
This script scrapes TDS-related discussions from the Discourse forum.
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
        logging.FileHandler('discourse_scraping.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Main function to scrape Discourse content."""
    logger.info("Starting TDS Discourse content scraping...")
    
    try:
        # Initialize scraper
        scraper = WebScraper()
        
        # Scrape discourse content
        logger.info(f"Scraping content from: {settings.discourse_url}")
        discourse_data = scraper.scrape_discourse_content()
        
        if discourse_data:
            # Save the scraped data
            scraper.save_scraped_data(discourse_data, "discourse_content.json")
            logger.info(f"Successfully scraped {len(discourse_data)} discourse topics")
            
            # Print summary
            print(f"\n=== Scraping Summary ===")
            print(f"Total topics scraped: {len(discourse_data)}")
            print(f"Data saved to: app/data/knowledge_base/discourse_content.json")
            print(f"Scraping completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Show sample of scraped content
            print(f"\n=== Sample Content ===")
            for i, item in enumerate(discourse_data[:3]):
                print(f"{i+1}. {item['title']}")
                print(f"   URL: {item['url']}")
                print(f"   Content preview: {item['content'][:150]}...")
                print()
                
            print(f"\n=== Important Note ===")
            print("This script currently uses sample data for demonstration.")
            print("For production use, implement actual Discourse API scraping")
            print("respecting rate limits and terms of service.")
            
        else:
            logger.warning("No content was scraped")
            
    except Exception as e:
        logger.error(f"Error during scraping: {e}")
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
