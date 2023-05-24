import sqlite3

conn = sqlite3.connect('database.db')

with open('db.sql') as f:
    conn.executescript(f.read())

# 创建一个执行句柄，用来执行后面的语句
cur = conn.cursor()

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('test1', 'hello1')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('test2', 'hello2')
            )

conn.commit()
conn.close()