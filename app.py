import sys
import sqlite3 as lite
from flask_login import LoginManager, UserMixin
from flask import Flask, redirect, render_template, request, session
# import functions for scraping the lenovo website
import scrape

app = Flask(__name__)
login_manage = LoginManager()


#username just for testing
username = "bennyhin"

# def main():
    # print(scrape.find_web_price(page_soup))
    # print(scrape.find_sale_price(page_soup))
    # print(scrape.find_processor_info(page_soup))
    # cur.execute("INSERT INTO users (username, password) VALUES ('asjdfkl', 'blah')")
    # con.commit()
    # con.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/history")
def history():
    return render_template("history.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")


@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    if request.method == "GET":
        return render_template("add_product.html")
    else:
        product_name = request.form.get('product_name')
        URL = request.form.get('url')
        if not product_name or not URL:
            return redirect("/apology")

        #insert information into database
        con = lite.connect("information.db")
        cur = con.cursor()
        cur.execute("INSERT INTO information (username, product_name, URL) VALUES (?, ?, ?)", (username, product_name, URL))
        con.commit()
        con.close()

        return redirect("/")


@app.route("/apology")
def apology():
    return render_template("apology.html")        


if __name__ == "__main__":
    app.run()