# 配置示例文件
# 复制此文件为 config.local.py 并根据需要修改

# Web服务器配置
WEB_HOST = '127.0.0.1'  # 仅本地访问，改为 '0.0.0.0' 允许局域网访问
WEB_PORT = 5000         # Web服务端口
DEBUG_MODE = True       # 开发模式，生产环境请设为 False

# 爬虫配置
DOWNLOAD_DELAY = 2      # 请求延迟（秒）
CONCURRENT_REQUESTS = 16  # 并发请求数
ROBOTSTXT_OBEY = False  # 是否遵循robots.txt

# 数据文件路径
DATA_FILE_PATH = 'amazon_scraper/games_data.json'

# User-Agent配置
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

# 如需自定义配置，请创建 config.local.py 文件并覆盖相应设置
