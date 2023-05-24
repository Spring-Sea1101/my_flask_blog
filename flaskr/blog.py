from flask import render_template, Flask
import sqlite3


app = Flask(__name__)


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
    conn = get_db_conn()
    posts = conn.execute('select * from posts').fetchall()
    return render_template("index.html", posts=posts)


@app.route('/posts/new', methods=('GET', 'POST'))
def new():
    return render_template('new.html')


@app.route('/posts/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)
