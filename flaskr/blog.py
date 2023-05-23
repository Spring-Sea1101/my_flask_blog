from flask import Flask


app = Flask(__name__)


@app.route('/')     # 装饰器，调用下面的函数
def index():
    return 'MyBlog'