from flask import Flask, render_template, request, jsonify
import json
import os
import re
from datetime import datetime, timedelta

app = Flask(__name__)

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
        '街机': ['arcade', 'classic', 'retro', 'jump', 'run', 'endless']
    }
    
    for category, keywords in categories.items():
        if any(keyword in title_lower for keyword in keywords):
            return category
    
    return '其他'

@app.route('/')
def index():
    # Load scraped data
    data_file = os.path.join(os.path.dirname(__file__), '..', 'amazon_scraper', 'games_data.json')
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            games = json.load(f)
            
        # 为每个游戏添加类型分类
        for game in games:
            game['category'] = extract_game_category(game['title'])
            
        # 获取所有唯一的游戏类型
        categories = sorted(list(set(game['category'] for game in games)))
        
    except FileNotFoundError:
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
    
    # 加载数据
    data_file = os.path.join(os.path.dirname(__file__), '..', 'amazon_scraper', 'games_data.json')
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            games = json.load(f)
    except FileNotFoundError:
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

if __name__ == '__main__':
    app.run(debug=True)
