#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
亚马逊游戏展示器 - 独立启动程序
无需Python环境，双击即可运行
"""

import os
import sys
import webbrowser
import threading
import time
from flask import Flask, render_template, request, jsonify
import json
import re

# 添加当前目录到Python路径
if hasattr(sys, '_MEIPASS'):
    # PyInstaller打包后的临时目录
    base_path = sys._MEIPASS
else:
    # 开发环境
    base_path = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, 
           template_folder=os.path.join(base_path, 'templates'),
           static_folder=os.path.join(base_path, 'static'))

def extract_game_category(title):
    """从游戏标题中提取游戏类型"""
    title_lower = title.lower()
    
    # 定义游戏类型关键词
    categories = {
        '赛车': ['racing', 'race', 'car', 'speed', 'drive', 'drift', 'rally'],
        '动作': ['action', 'fight', 'battle', 'war', 'shoot', 'attack', 'combat', 'ninja', 'hero'],
        '冒险': ['adventure', 'quest', 'explore', 'journey', 'treasure'],
        '益智': ['puzzle', 'match', 'merge', 'brain', 'logic', 'word', 'trivia', 'quiz'],
        '策略': ['strategy', 'tower', 'defense', 'build', 'empire', 'civilization'],
        '模拟': ['simulation', 'sim', 'tycoon', 'farm', 'city', 'life', 'manage'],
        '体育': ['sports', 'football', 'soccer', 'basketball', 'tennis', 'golf', 'baseball'],
        '博彩': ['casino', 'poker', 'slots', 'blackjack', 'bingo', 'lottery'],
        '角色扮演': ['rpg', 'role', 'fantasy', 'magic', 'dragon', 'knight', 'legend'],
        '街机': ['arcade', 'classic', 'jump', 'run', 'endless']
    }
    
    for category, keywords in categories.items():
        if any(keyword in title_lower for keyword in keywords):
            return category
    
    return '其他'

@app.route('/')
def index():
    # 查找游戏数据文件
    data_file = None
    possible_paths = [
        os.path.join(base_path, 'games_data.json'),
        os.path.join(os.path.dirname(base_path), 'games_data.json'),
        os.path.join(os.path.dirname(__file__), 'games_data.json'),
        'games_data.json'
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            data_file = path
            break
    
    try:
        if data_file:
            with open(data_file, 'r', encoding='utf-8') as f:
                games = json.load(f)
        else:
            games = []
            
        # 为每个游戏添加类型分类
        for game in games:
            game['category'] = extract_game_category(game['title'])
            
        # 获取所有唯一的游戏类型
        categories = sorted(list(set(game['category'] for game in games)))
        
    except (FileNotFoundError, json.JSONDecodeError):
        games = []
        categories = []
    
    return render_template('index.html', games=games, categories=categories)

@app.route('/api/filter')
def filter_games():
    """API端点用于筛选游戏"""
    # 获取筛选参数
    min_reviews = request.args.get('min_reviews', 0, type=int)
    max_reviews = request.args.get('max_reviews', type=int)
    category = request.args.get('category', '')
    price_type = request.args.get('price_type', 'all')  # all, free, paid
    release_date_filter = request.args.get('release_date', '')  # YYYY-MM format
    
    # 查找游戏数据文件
    data_file = None
    possible_paths = [
        os.path.join(base_path, 'games_data.json'),
        os.path.join(os.path.dirname(base_path), 'games_data.json'),
        os.path.join(os.path.dirname(__file__), 'games_data.json'),
        'games_data.json'
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            data_file = path
            break
    
    try:
        if data_file:
            with open(data_file, 'r', encoding='utf-8') as f:
                games = json.load(f)
        else:
            return jsonify([])
    except (FileNotFoundError, json.JSONDecodeError):
        return jsonify([])
    
    # 为每个游戏添加类型分类
    for game in games:
        game['category'] = extract_game_category(game['title'])
    
    # 应用筛选条件
    filtered_games = []
    for game in games:
        # 评论数筛选
        if game['reviews'] < min_reviews:
            continue
        if max_reviews and game['reviews'] > max_reviews:
            continue
            
        # 类型筛选
        if category and game['category'] != category:
            continue
            
        # 价格类型筛选
        if price_type == 'free' and game['price'] != '$0.00':
            continue
        elif price_type == 'paid' and game['price'] == '$0.00':
            continue
        
        # 发布时间筛选
        if release_date_filter:
            game_release_date = game.get('release_date')
            if game_release_date:
                try:
                    # 将用户输入的YYYY-MM转换为YYYY-MM-01格式进行比较
                    filter_date = f"{release_date_filter}-01"
                    if game_release_date < filter_date:
                        continue
                except:
                    # 如果日期解析失败，跳过该游戏
                    continue
            else:
                # 如果游戏没有发布时间信息，在筛选发布时间时跳过
                continue
            
        filtered_games.append(game)
    
    return jsonify(filtered_games)

def open_browser():
    """延迟打开浏览器"""
    time.sleep(1.5)  # 等待Flask启动
    webbrowser.open('http://127.0.0.1:5000')

def main():
    """主函数"""
    print("========================================")
    print("    🎮 亚马逊游戏展示器 - 独立版")
    print("========================================")
    print()
    print("正在启动Web服务器...")
    print("浏览器将自动打开页面")
    print()
    print("访问地址: http://127.0.0.1:5000")
    print("按 Ctrl+C 可停止服务器")
    print("========================================")
    
    # 在新线程中打开浏览器
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # 启动Flask应用
    try:
        app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except Exception as e:
        print(f"启动失败: {e}")
        input("按任意键退出...")

if __name__ == '__main__':
    main()
