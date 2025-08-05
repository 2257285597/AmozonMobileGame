# 部署和配置指南

## 🌐 本地环境配置详解

### 网络服务配置

#### 默认配置
- **地址**: `127.0.0.1` (仅本机访问)
- **端口**: `5000`
- **协议**: HTTP

#### 修改配置方法

1. **修改Web应用配置** (`web_app/app.py`):
   ```python
   if __name__ == '__main__':
       app.run(
           host='127.0.0.1',    # 修改为 '0.0.0.0' 允许外部访问
           port=5000,           # 修改端口号
           debug=True           # 生产环境改为 False
       )
   ```

2. **修改独立应用配置** (`standalone_app.py`):
   ```python
   app.run(
       host='127.0.0.1', 
       port=5000, 
       debug=False, 
       use_reloader=False
   )
   ```

### 🔒 安全配置

#### 生产环境建议
```python
# 生产环境配置
app.run(
    host='127.0.0.1',  # 仅本地访问更安全
    port=5000,
    debug=False,       # 关闭调试模式
    threaded=True      # 启用多线程
)
```

#### 局域网访问配置
```python
# 允许局域网访问（谨慎使用）
app.run(
    host='0.0.0.0',    # 监听所有网卡
    port=5000,
    debug=False
)
```

### 📁 文件路径配置

#### 数据文件路径
- **爬取数据**: `amazon_scraper/games_data.json`
- **模板文件**: `web_app/templates/`
- **静态文件**: `web_app/static/`

#### 路径自定义
在 `web_app/app.py` 中修改：
```python
# 自定义数据文件路径
data_file = os.path.join(os.path.dirname(__file__), '..', 'amazon_scraper', 'games_data.json')

# 或绝对路径
data_file = r'C:\path\to\your\games_data.json'
```

### 🕷️ 爬虫配置详解

#### 核心配置文件: `amazon_scraper/amazon_scraper/settings.py`

```python
# 基本配置
BOT_NAME = "amazon_scraper"
ROBOTSTXT_OBEY = False

# 性能配置
DOWNLOAD_DELAY = 2                    # 请求间隔
RANDOMIZE_DOWNLOAD_DELAY = True       # 随机延迟
CONCURRENT_REQUESTS = 16              # 并发数

# 请求头配置
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

# 自动限速配置
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
```

## 🐳 Docker部署 (可选)

### Dockerfile 示例
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "web_app/app.py"]
```

### docker-compose.yml 示例
```yaml
version: '3.8'
services:
  amazon-scraper:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./amazon_scraper:/app/amazon_scraper
    environment:
      - FLASK_ENV=production
```

## 🔧 环境变量配置

### 支持的环境变量
```bash
# Flask配置
FLASK_APP=web_app/app.py
FLASK_ENV=development
FLASK_DEBUG=1

# 自定义配置
WEB_HOST=127.0.0.1
WEB_PORT=5000
DATA_PATH=amazon_scraper/games_data.json
```

### Windows批处理配置
在 `start_web.bat` 中添加：
```batch
set FLASK_ENV=production
set WEB_PORT=8080
```

## 📊 监控和日志

### 启用日志记录
在 `web_app/app.py` 中添加：
```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

app.logger.setLevel(logging.INFO)
```

### 性能监控
```python
from flask import g
import time

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    total_time = time.time() - g.start_time
    app.logger.info(f'Request took {total_time:.2f}s')
    return response
```

## 🚀 自动化部署脚本

### 完整部署脚本 (deploy.bat)
```batch
@echo off
echo 开始部署亚马逊游戏爬虫...

REM 创建虚拟环境
python -m venv venv
call venv\Scripts\activate

REM 安装依赖
pip install -r requirements.txt

REM 运行爬虫
cd amazon_scraper
scrapy crawl amazon_games -o games_data.json

REM 启动Web服务
cd ..\web_app
start python app.py

echo 部署完成！访问 http://127.0.0.1:5000
pause
```
