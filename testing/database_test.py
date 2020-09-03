import sqlite3 as lite
import sys

con = lite.connect('test.db')

with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM test")
    rows = cur.fetchall()
    print(rows[0][1])