import sqlite3

with open('init.sql', 'r', encoding='utf-8') as f:
    sql = f.read()

conn = sqlite3.connect('./test.db')
try:
    conn.executescript(sql)
finally:
    conn.close()