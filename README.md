# 🎮 Amazon Mobile Games Scraper

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![Scrapy](https://img.shields.io/badge/Scrapy-2.0+-red.svg)](https://scrapy.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🌟 项目概述

这是一个完整的亚马逊手机游戏数据爬取和展示系统，提供中文界面和智能筛选功能。

**主要特性：**
- 🕷️ 基于Scrapy的高效爬虫系统
- 🌐 Flask Web界面，支持实时筛选
- 📊 丰富的数据统计和可视化
- 🎯 多维度智能筛选（价格、类型、评论数、时间）
- 📦 支持打包为独立可执行文件

## 🛠️ 环境要求

- Python 3.8+
- Windows系统（批处理文件适配）

## 📦 安装步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/your-username/amazon-mobile-games-scraper.git
   cd amazon-mobile-games-scraper
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ 重要配置说明

### 🌐 网络服务配置
- **默认地址**: `http://127.0.0.1:5000`
- **端口**: `5000`（可在代码中修改）
- **访问限制**: 仅本地访问（localhost）

### 📁 数据文件路径
- **爬取数据**: `amazon_scraper/games_data.json`
- **模板文件**: `web_app/templates/`
- **静态资源**: `web_app/static/`

### 🕷️ 爬虫配置
- **请求延迟**: 2秒（防止被封IP）
- **User-Agent**: 已配置Chrome浏览器标识
- **robots.txt**: 已禁用遵循（`ROBOTSTXT_OBEY = False`）

### 🔧 环境变量说明
项目无需额外环境变量配置，所有配置已内置。如需自定义：
- 修改 `web_app/app.py` 中的 `app.run()` 参数调整端口
- 修改 `amazon_scraper/amazon_scraper/settings.py` 调整爬虫行为

## �🚀 快速启动

### 方法1: 完整启动（首次使用）
```bash
run.bat
```
> 执行完整流程：爬取数据 + 启动Web应用

### 方法2: 仅启动Web（推荐日常使用）
```bash
start_web.bat
```
> 仅启动Web应用，使用已有的JSON数据

### 方法3: 独立可执行版（无需Python环境）
```bash
build_standalone.bat
```
> 打包成独立exe文件，双击即可运行，无需配置环境

### 方法4: 手动启动
1. **启动爬虫**
   ```bash
   cd amazon_scraper
   scrapy crawl amazon_games -o games_data.json
   ```

2. **启动Web应用**
   ```bash
   cd web_app
   python app.py
   ```

3. **访问应用**
   打开浏览器访问: http://127.0.0.1:5000

## 🎯 主要功能

### 📊 数据统计面板
- **游戏总数**: 显示爬取的游戏总数
- **当前显示**: 筛选后显示的游戏数量
- **免费游戏**: 免费游戏数量统计
- **平均评论数**: 当前显示游戏的平均评论数

### 🔍 智能筛选系统

#### 1. 评论数筛选
- **最少评论数**: 设置评论数下限
- **最多评论数**: 设置评论数上限
- **用途**: 找到热门度适中的游戏

#### 2. 游戏类型筛选
基于标题关键词智能分类：
| 中文类型 | 关键词示例 |
|---------|-----------|
| 赛车 | racing, car, speed, drive |
| 动作 | action, fight, battle, war |
| 冒险 | adventure, quest, explore |
| 益智 | puzzle, match, brain, logic |
| 策略 | strategy, tower, defense |
| 模拟 | simulation, farm, city, life |
| 体育 | sports, football, basketball |
| 博彩 | casino, poker, slots |
| 角色扮演 | rpg, fantasy, magic |
| 街机 | arcade, classic, retro |
| 其他 | 未分类游戏 |

#### 3. 价格类型筛选
- **所有游戏**: 显示全部游戏
- **仅免费**: 只显示免费游戏 ($0.00)
- **仅付费**: 只显示付费游戏

#### 4. 发布时间筛选
- **时间选择器**: 选择年月（YYYY-MM格式）
- **筛选逻辑**: 显示在指定时间之后发布的游戏
- **用途**: 查找最新发布的游戏或特定时期的游戏

## 💡 使用技巧

### 精准筛选示例

**寻找热门免费游戏**
```
最少评论数: 1000
价格类型: 仅免费
```

**寻找优质赛车游戏**
```
游戏类型: 赛车
最少评论数: 500
```

**寻找轻度益智游戏**
```
游戏类型: 益智
价格类型: 仅免费
最少评论数: 100
最多评论数: 5000
```

**寻找最新发布的游戏**
```
发布时间: 2024-01（2024年1月之后）
最少评论数: 10
```

**寻找经典老游戏**
```
发布时间: 2020-01（2020年1月之后）
最少评论数: 1000
```

### 快捷操作
- **回车键**: 在任何筛选框中按回车可快速应用筛选
- **重置按钮**: 一键清除所有筛选条件
- **实时统计**: 筛选后统计数据自动更新

## 🎨 界面特色

### 响应式设计
- 🖥️ 桌面端完美适配
- 📱 移动端友好界面
- 📊 现代化卡片布局

### 视觉效果
- 🎨 渐变色筛选面板
- ✨ 悬停动画效果
- 📈 实时加载指示器
- 🎯 清晰的游戏分类标签

## 📁 项目结构

```
scraper_project/
├── run.bat                    # 完整启动脚本（爬取+Web）
├── start_web.bat             # 仅Web启动脚本（推荐日常使用）
├── build_standalone.bat      # 独立版打包脚本
├── standalone_app.py         # 独立版主程序
├── standalone_app.spec       # PyInstaller配置文件
├── requirements_standalone.txt # 独立版依赖
├── 独立版使用说明.md          # 独立版使用文档
├── requirements.txt          # Python依赖包
├── amazon_scraper/           # Scrapy爬虫
│   ├── games_data.json      # 爬取的游戏数据
│   └── amazon_scraper/
│       └── spiders/
│           └── games_spider.py
└── web_app/                 # Flask Web应用
    ├── app.py              # 主应用文件
    ├── templates/
    │   └── index.html      # 中文界面模板
    └── static/             # 静态文件
```

## 🔧 技术栈

### 后端技术
- **Python 3.x**: 主要编程语言
- **Scrapy**: 网页爬虫框架
- **Flask**: Web应用框架
- **Requests**: HTTP请求库

### 前端技术
- **Bootstrap 5**: UI框架
- **Font Awesome**: 图标库
- **JavaScript ES6**: 交互逻辑
- **CSS3**: 样式和动画

### 数据处理
- **JSON**: 数据存储格式
- **正则表达式**: 文本分析
- **智能分类**: 基于关键词的游戏分类

## 📈 数据来源

- **来源**: Amazon移动游戏商店
- **更新方式**: 运行 `run.bat` 重新爬取
- **数据字段**: 标题、价格、评论数、图片链接、发布时间
- **分类方式**: 基于游戏标题关键词自动分类
- **时间获取**: 自动解析游戏发布时间信息

## 🛠️ 维护和更新

### 更新游戏数据
```bash
# 删除旧数据
cd amazon_scraper
del games_data.json

# 重新爬取
..\venv\Scripts\scrapy crawl amazon_games -o games_data.json
```

### 自定义爬取参数
```bash
# 爬取更多页面
..\venv\Scripts\scrapy crawl amazon_games -a max_pages=5 -o games_data.json

# 设置最小评论数
..\venv\Scripts\scrapy crawl amazon_games -a min_reviews=50 -o games_data.json
```

## 🎉 特色亮点

✅ **完全中文化** - 界面、提示、分类全部中文显示  
✅ **智能分类** - 自动识别游戏类型，无需人工标注  
✅ **多维筛选** - 评论数、类型、价格、发布时间四重筛选  
✅ **实时统计** - 动态显示筛选结果统计信息  
✅ **响应式设计** - 支持各种设备完美显示  
✅ **一键部署** - run.bat脚本自动化所有流程  
✅ **独立可执行** - 无需Python环境，双击即可运行  

## 🚨 疑难解答

### 常见问题

**Q: 访问 http://127.0.0.1:5000 提示无法连接？**
```bash
# 检查Python环境
python --version

# 检查Flask是否安装
pip show flask

# 检查端口是否被占用
netstat -ano | findstr :5000
```

**Q: 爬虫无法获取数据？**
```bash
# 检查网络连接
ping amazon.com

# 检查Scrapy版本
pip show scrapy

# 手动测试爬虫
cd amazon_scraper
scrapy crawl amazon_games -L INFO
```

**Q: 独立exe文件无法运行？**
- 确保已运行 `build_standalone.bat`
- 检查防火墙/杀毒软件是否阻止
- 查看 `build/standalone_app/warn-standalone_app.txt` 日志

**Q: 数据显示为空？**
- 确认 `amazon_scraper/games_data.json` 文件存在
- 检查JSON文件格式是否正确
- 重新运行爬虫更新数据

### 端口配置

**修改默认端口 (5000):**

1. **修改Web应用端口**:
   编辑 `web_app/app.py` 最后一行:
   ```python
   app.run(debug=True, port=8080)  # 改为8080端口
   ```

2. **修改独立应用端口**:
   编辑 `standalone_app.py` 第190行:
   ```python
   app.run(host='127.0.0.1', port=8080, debug=False, use_reloader=False)
   ```

3. **修改批处理文件提示**:
   相应更新 `start_web.bat` 中的访问地址提示

### 网络配置

**允许局域网访问:**
```python
# 修改 app.run() 参数
app.run(host='0.0.0.0', port=5000, debug=True)
```
⚠️ **安全警告**: 仅在受信任的网络环境中使用

## 📝 版本信息

- **当前版本**: v1.0.0  
- **Python版本**: 3.8+  
- **主要依赖**: Scrapy 2.11.0, Flask 3.0.2  
- **兼容系统**: Windows 10/11  

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源协议。
✅ **时间筛选** - 根据游戏发布时间精准筛选  

## 📞 使用说明

### 开发者使用
1. **首次使用**: 运行 `run.bat` 完成环境搭建和数据爬取
2. **日常使用**: 运行 `start_web.bat` 直接启动Web应用，访问 http://127.0.0.1:5000
3. **数据更新**: 运行 `run.bat` 更新游戏数据
4. **快速启动**: 如果已有数据，推荐使用 `start_web.bat` 快速启动

### 用户分发版
1. **打包独立版**: 运行 `build_standalone.bat` 创建独立可执行文件
2. **分发给用户**: 将 `dist` 文件夹整个复制给用户
3. **用户使用**: 双击 `亚马逊游戏展示器.exe` 即可运行
4. **无需环境**: 用户无需安装Python或任何依赖

### 📦 独立版特色
- 🚀 **一键运行**: 双击exe文件即可启动
- 🌐 **自动打开**: 程序会自动打开浏览器页面
- 📱 **完整功能**: 包含所有筛选和展示功能
- 💾 **数据内置**: 游戏数据打包在程序中
- 🔒 **安全可靠**: 无需联网，本地运行

🎮 **开始你的游戏发现之旅吧！**
