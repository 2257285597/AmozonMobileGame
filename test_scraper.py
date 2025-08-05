#!/usr/bin/env python3
"""
Test script to check if the scraper is working correctly
"""
import subprocess
import json
import os
import sys

def test_scraper():
    print("Testing Amazon Games Scraper...")
    
    # Change to the scraper directory
    scraper_dir = os.path.join(os.path.dirname(__file__), 'amazon_scraper')
    
    # Clear existing data
    data_file = os.path.join(scraper_dir, 'games_data.json')
    with open(data_file, 'w') as f:
        f.write('[]')
    
    # Run the scraper with minimal settings
    cmd = [
        sys.executable, '-m', 'scrapy', 'crawl', 'amazon_games',
        '-a', 'min_reviews=0',  # Accept all games
        '-a', 'max_pages=1',    # Just test one page
        '-o', 'games_data.json'
    ]
    
    try:
        print(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(cmd, cwd=scraper_dir, capture_output=True, text=True)
        
        print(f"Return code: {result.returncode}")
        print(f"STDOUT:\n{result.stdout}")
        
        if result.stderr:
            print(f"STDERR:\n{result.stderr}")
        
        # Check if data was scraped
        if os.path.exists(data_file):
            with open(data_file, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    print(f"\nScraped {len(data)} items")
                    
                    if data:
                        print("\nFirst few items:")
                        for i, item in enumerate(data[:3]):
                            print(f"{i+1}. {item}")
                    else:
                        print("No items were scraped")
                        
                except json.JSONDecodeError:
                    print("Invalid JSON in output file")
        else:
            print("Output file not created")
            
    except Exception as e:
        print(f"Error running scraper: {e}")

if __name__ == "__main__":
    test_scraper()
