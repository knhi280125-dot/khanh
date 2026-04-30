from flask import Flask, render_template, request
from pymongo import MongoClient
import certifi
from datetime import datetime

app = Flask(__name__)

# MongoDB 連線
uri = "mongodb+srv://knhi280125_db_user:x3N6DpTxIzBlfzZ7@cluster0.bdra68f.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, tlsCAFile=certifi.where())
db = client['movie_db']
movies_col = db['movies']

@app.route('/')
def index():
    return render_template('index.html')

# --- Nhóm nút màu Xanh (Thông tin) ---
@app.route('/mis')
def mis():
    return render_template('mis.html') # Trang em vừa chụp ảnh cho anh xem

@app.route('/today')
def today():
    now = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
    return f"<h1>今天的日期時間是：{now}</h1><br><a href='/'>返回首頁</a>"

# --- Nhóm nút màu Tím (Bài tập Movie - QUAN TRỌNG) ---
@app.route('/movie2')
def movie2():
    upcoming_movies = [
        {"title": "死侍與鋼鐵人", "release_date": "2024-07-26"},
        {"title": "小丑：雙重瘋狂", "release_date": "2024-10-04"},
        {"title": "海洋奇緣 2", "release_date": "2024-11-27"}
    ]
    movies_col.delete_many({})
    movies_col.insert_many(upcoming_movies)
    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template('movie2.html', movies=upcoming_movies, update_time=update_time)

@app.route('/movie3', methods=['GET', 'POST'])
def movie3():
    query_result = []
    keyword = ""
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        query_result = list(movies_col.find({"title": {"$regex": keyword, "$options": "i"}}))
    return render_template('movie3.html', movies=query_result, keyword=keyword)

# Các route khác em có thể thêm tương tự...
