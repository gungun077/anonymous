from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# 데이터베이스 초기화
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        content = request.form['content']
        if content:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (content) VALUES (?)', (content,))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts ORDER BY timestamp DESC').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def post_detail(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    if post is None:
        return "게시글을 찾을 수 없습니다.", 404
    return render_template('post.html', post=post)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
