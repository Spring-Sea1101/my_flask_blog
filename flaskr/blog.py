from flask import render_template, Flask, request, url_for, flash, redirect, g, session
from dataclasses import dataclass
import sqlite3


app = Flask(__name__)
app.config['SECRET_KEY'] = 'sonodaumi'  # 密钥，加密字符串


@dataclass
class User:
    id: int
    username: str
    password: str

users = [
    User(1, "Harumi", "sonodaumi1101"),
]


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        user = [u for u in users if u.id == session['user_id']][0]
        g.user = user


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 登录
        session.pop('user_id', None)
        username = request.form.get("username", None)
        password = request.form.get("password", None)
        user = [u for u in users if u.username==username]
        if len(user) > 0:
            user = user[0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('index'))

    return render_template("login.html")


def get_db_conn():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = get_db_conn()
    post = conn.execute('select * from posts where id = ?', (post_id,)).fetchone()
    return post


@app.route("/")
def index():
    if not g.user:
        return redirect(url_for('login'))

    conn = get_db_conn()
    posts = conn.execute('select * from posts').fetchall()
    return render_template("index.html", posts=posts)


@app.route('/posts/new', methods=('GET', 'POST'))
def new():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('标题不能为空')
        elif not content:
            flash('内容不能为空')
        else:
            conn = get_db_conn()
            conn.execute('insert into posts (title, content) values (?, ?)', (title, content))
            conn.commit()
            conn.close()
            flash('文章发布成功')
            return redirect(url_for('index'))


    return render_template('new.html')


@app.route('/posts/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)
