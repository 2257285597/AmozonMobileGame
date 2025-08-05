import scrapy
from scrapy.http import Request
from urllib.parse import urlencode
import json
import re
from datetime import datetime

class GamesSpider(scrapy.Spider):
    name = "amazon_games"
    
    def __init__(self, *args, **kwargs):
        self.current_page = 1
        self.max_pages = int(kwargs.pop('max_pages', 10))
        super().__init__(*args, **kwargs)
    
    def start_requests(self):
        # Use a simpler search for mobile games/apps
        base_url = "https://www.amazon.com/s"
        params = {
            'k': 'mobile games',
            'i': 'mobile-apps',
            'ref': 'sr_pg_1'
        }
        
        # Allow customization via spider arguments
        page = getattr(self, 'page', 1)
        min_reviews = getattr(self, 'min_reviews', 0)
        
        params['page'] = page
        url = f"{base_url}?{urlencode(params)}"
        
        yield Request(url, self.parse, meta={'min_reviews': min_reviews})

    def parse(self, response):
        min_reviews = int(response.meta['min_reviews'])
        
        # Extract game data with more flexible selectors
        games = response.css('div[data-component-type="s-search-result"]')
        if not games:
            self.logger.warning(f"No games found on page {response.url}")
            return
            
        for game in games:
            try:
                # Try multiple selector patterns for title
                title = (game.css('h2 a span::text').get() or 
                        game.css('h2 span::text').get() or
                        game.css('.a-size-medium::text').get() or
                        game.css('.a-size-base-plus::text').get() or
                        game.css('.s-size-mini .a-color-base::text').get())
                
                # Get reviews count
                reviews_text = game.css('a[href*="#customerReviews"] span::text').get()
                reviews = 0
                if reviews_text:
                    try:
                        # Extract only digits and commas from the text
                        num_str = ''.join(c for c in reviews_text if c.isdigit() or c == ',')
                        reviews = int(num_str.replace(',', '')) if num_str else 0
                    except ValueError:
                        reviews = 0
                
                # Get price
                price = (game.css('.a-price .a-offscreen::text').get() or
                        game.css('.a-price-whole::text').get() or
                        'Free')
                
                # Get link - try multiple selectors
                link_href = (game.css('h2 a::attr(href)').get() or
                           game.css('a[data-csa-c-type="link"]::attr(href)').get() or
                           game.css('.a-link-normal::attr(href)').get() or
                           game.css('a[href*="/dp/"]::attr(href)').get())
                link = response.urljoin(link_href) if link_href else None
                
                # Get image
                image = game.css('img::attr(src)').get()
                
                # Try to get release date from various places
                release_date = None
                release_date_text = None
                
                # Look for date in different formats
                date_selectors = [
                    '.a-color-tertiary .a-size-base::text',
                    '.a-color-secondary .a-size-base::text', 
                    '.a-text-bold + .a-size-base::text',
                    '.a-section .a-size-base::text'
                ]
                
                for selector in date_selectors:
                    date_texts = game.css(selector).getall()
                    for text in date_texts:
                        if text and any(month in text.lower() for month in ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']):
                            release_date_text = text.strip()
                            break
                    if release_date_text:
                        break
                
                # Parse the date
                if release_date_text:
                    try:
                        # Try different date formats
                        date_patterns = [
                            r'(\w+)\s+(\d{1,2}),\s*(\d{4})',  # "Jan 15, 2023"
                            r'(\d{1,2})\s+(\w+)\s+(\d{4})',   # "15 Jan 2023"
                            r'(\w+)\s+(\d{4})',               # "Jan 2023"
                        ]
                        
                        for pattern in date_patterns:
                            match = re.search(pattern, release_date_text)
                            if match:
                                groups = match.groups()
                                if len(groups) == 3:
                                    month_str, day_str, year_str = groups
                                    if month_str.isdigit():
                                        day_str, month_str = month_str, day_str
                                elif len(groups) == 2:
                                    month_str, year_str = groups
                                    day_str = "1"
                                
                                # Convert month name to number
                                month_map = {
                                    'jan': 1, 'january': 1, 'feb': 2, 'february': 2, 'mar': 3, 'march': 3,
                                    'apr': 4, 'april': 4, 'may': 5, 'jun': 6, 'june': 6, 'jul': 7, 'july': 7,
                                    'aug': 8, 'august': 8, 'sep': 9, 'september': 9, 'oct': 10, 'october': 10,
                                    'nov': 11, 'november': 11, 'dec': 12, 'december': 12
                                }
                                
                                month_num = month_map.get(month_str.lower(), None)
                                if month_num:
                                    release_date = f"{year_str}-{month_num:02d}-{day_str.zfill(2)}"
                                break
                    except:
                        pass

                item = {
                    'title': title.strip() if title else None,
                    'price': price,
                    'reviews': reviews,
                    'link': link,
                    'image': image,
                    'release_date': release_date
                }

                # Only require title to be present (more lenient validation)
                if item['title'] and len(item['title']) > 3:  # Basic title validation
                    if reviews >= min_reviews:
                        yield item
                        self.logger.info(f"Scraped: {item['title']} - Reviews: {reviews}")
                    else:
                        self.logger.debug(f"Skipping item with {reviews} reviews (min required: {min_reviews})")
                else:
                    self.logger.debug(f"Skipping item without valid title: {item}")
                    
            except Exception as e:
                self.logger.error(f"Error processing game item: {e}")
        
        # Pagination
        self.current_page += 1
        next_page = response.css('a.s-pagination-next::attr(href)').get()
        if next_page and self.current_page <= self.max_pages:
            yield response.follow(next_page, self.parse, meta={'min_reviews': min_reviews})
