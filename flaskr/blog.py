from flask import render_template, Flask, request, url_for, flash, redirect
import sqlite3


app = Flask(__name__)
app.config['SECRET_KEY'] = 'sonodaumi'  # 密钥，加密字符串


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
