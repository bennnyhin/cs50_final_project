import sys
import sqlite3 as lite
from flask_login import LoginManager, UserMixin
from flask import Flask, redirect, render_template, request, session
# import functions for scraping the lenovo website
import scrape

app = Flask(__name__)
login_manage = LoginManager()


#username just for testing
username = "testing"

# print(scrape.find_sale_price(page_soup))
# print(scrape.find_processor_info(page_soup))
# cur.execute("INSERT INTO users (username, password) VALUES ('asjdfkl', 'blah')")
# con.commit()
# con.close()


@app.route("/")
def index():
    con = lite.connect("information.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM information WHERE username='%s'" % username)
    information = cur.fetchall()

    #create list of everything
    url_list = []
    product_list = []
    for info in information:
        product_list.append(info[2])
        url_list.append(info[3])

    #get all information on the products associated with user in database
    web_price_list = []
    sale_price_list = []
    processor_list = []
    for i in range(len(information)):
        web_price_list.append(scrape.find_web_price(scrape.find_html(url_list[i])))
        sale_price_list.append(scrape.find_sale_price(scrape.find_html(url_list[i])))
        processor_list.append(scrape.find_processor_info(scrape.find_html(url_list[i])))

    #put all lists into a dictionary
    product_info = {}
    product_info["product"] = product_list
    product_info["old_price"] = web_price_list
    product_info["sale_price"] = sale_price_list
    product_info["processor"] = processor_list

    con.close()
    
    #return the dictionary of all of the product info and the number of products associated with the user
    return render_template("index.html", product_info=product_info, num_product=len(information))


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