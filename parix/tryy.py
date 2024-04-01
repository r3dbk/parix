import sqlite3

conn = sqlite3.connect('parix.py')

cur = conn.cursor()
print(cur.execute('SELECT * FROM master_db;').fetchall())
