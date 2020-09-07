from apscheduler.schedulers.blocking import BlockingScheduler
import sqlite3 as lite

def insert():
    con = lite.connect("testing.db")
    cur = con.cursor()
    cur.execute("INSERT INTO test (user) VALUES ('test')")
    con.commit()
    con.close()


def testing():
    print("Hello world")

scheduler = BlockingScheduler()
scheduler.add_job(testing, 'interval', hours=0.0166666666)
scheduler.add_job(insert, 'interval', hours=0.001)
scheduler.start()