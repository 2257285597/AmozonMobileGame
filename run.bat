@echo off
echo Starting Amazon Games Scraper...

REM Clear previous data
echo Clearing previous data...
if exist "amazon_scraper\games_data.json" del "amazon_scraper\games_data.json"

REM Run the scraper (max 50 pages to get more data)
echo Running scraper...
cd amazon_scraper
python -m scrapy crawl amazon_games -a min_reviews=0 -a max_pages=400 -o games_data.json
if %ERRORLEVEL% neq 0 (
    echo Scraper failed with error code %ERRORLEVEL%
    cd ..
    pause
    exit /b 1
)
cd ..

REM Check if data was scraped
echo Checking scraped data...
for %%A in (amazon_scraper\games_data.json) do set size=%%~zA
if %size% lss 10 (
    echo No data was scraped. Check the logs in amazon_scraper\scrapy.log
    pause
    exit /b 1
)

echo Scraping completed successfully!
echo Checking scraped data...
for %%A in (amazon_scraper\games_data.json) do set size=%%~zA
if %size% lss 10 (
    echo No data was scraped. Check the logs in amazon_scraper\scrapy.log
    pause
    exit /b 1
)

echo Scraping completed successfully!
echo Starting web application...
echo Open your browser and go to: http://127.0.0.1:5000

REM Run the web app
cd web_app
..\venv\Scripts\python app.py
