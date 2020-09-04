import sys
import sqlite3 as lite
from flask_login import LoginManage, UserMixin
from flask import Flask, redirect, render_template, request, session
# import functions for scraping the lenovo website
import scrape

app = Flask(__name__)
login_manage = LoginManager()

#initiate the database to be accessed
con = lite.connect("information.db")
cur = con.cursor()

def main():
    # page_soup = scrape.find_html("https://www.lenovo.com/ca/en/laptops/thinkpad/thinkpad-x1/X1-Yoga-Gen-5/p/22TP2X1X1Y5")
    # print(scrape.find_web_price(page_soup))
    # print(scrape.find_sale_price(page_soup))
    # print(scrape.find_processor_info(page_soup))
    # cur.execute("INSERT INTO users (username, password) VALUES ('ben', 'blah')")

    con.commit()
    con.close()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("login.html")
    else:





# @app.route("/login", methods=["GET", "POST"])
# def login():



if __name__ == "__main__":
    main()