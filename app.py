import sys, atexit
import sqlite3 as lite
from flask_login import LoginManager, UserMixin
from flask import Flask, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

# import functions for scraping the lenovo website
import scrape

username_global = None 

# this function is called every day and added to the history table in the database
def add_history():
    con = lite.connect("information.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM information WHERE username='%s'" % username_global)
    information = cur.fetchall()

    #create list of everything
    url_list = []
    product_list = []
    for info in information:
        product_list.append(info[2])
        url_list.append(info[3])

    #get all information on the products associated with user in database with information on website right now
    web_price_list = []
    sale_price_list = []
    processor_list = []
    for i in range(len(information)):
        page_soup = scrape.find_html(url_list[i])
        number = scrape.find_base_model(page_soup)
        web_price_list.append(scrape.find_web_price(page_soup, number))
        sale_price_list.append(scrape.find_sale_price(page_soup, number))
        processor_list.append(scrape.find_processor_info(page_soup, number))

    for j in range(len(information)):
        cur.execute("INSERT INTO history (username, product, sale_price, web_price) VALUES (?, ?, ?,?);", (username_global, product_list[j], sale_price_list[j], web_price_list[j]))
    con.commit()
    con.close()
    print("added to database")


app = Flask(__name__)
app.secret_key = "asfdjklasdjflasdkf"


@app.route("/")
def index():
    if "user" in session and username_global is not None:
        return redirect("/main")
    else:
        return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation_password = request.form.get("confirmation-password")

        #error checking
        if not username:
            return redirect("/apology")
        if not password:
            return redirect("/apology")
        if not confirmation_password:
            return redirect("/apology")
        if password != confirmation_password:
            return redirect("/apology")
        
        pass_hash = generate_password_hash(password)
        con = lite.connect("information.db")
        cur = con.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?);", (username, pass_hash))
        con.commit()
        con.close()

        return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        if not username:
            return redirect("/apology")
        if not password:
            return redirect("/apology")
        
        con = lite.connect("information.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE username='%s';" % username)
        information = cur.fetchall()

        for info in information:
            hash_pass = info[2]
        
        if check_password_hash(hash_pass, password):
            global username_global
            username_global = username
            session["user"] = username
            return redirect("/")
            
        return redirect("/apology")


@app.route("/main")
def main():
    con = lite.connect("information.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM information WHERE username='%s'" % username_global)
    information = cur.fetchall()

    #create list of everything
    url_list = []
    product_list = []

    for info in information:
        product_list.append(info[2])
        url_list.append(info[3])

    #get all information on the products associated with user in database with information on website right now
    web_price_list = []
    sale_price_list = []
    processor_list = []
    for i in range(len(information)):
        page_soup = scrape.find_html(url_list[i])
        number = scrape.find_base_model(page_soup)
        web_price_list.append(scrape.find_web_price(page_soup, number))
        sale_price_list.append(scrape.find_sale_price(page_soup, number))
        processor_list.append(scrape.find_processor_info(page_soup, number))

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
    con = lite.connect("information.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM history WHERE username='%s'" % username_global)
    information = cur.fetchall()

    #creating list of everything
    product_name_list = []
    price_list = []
    date_list = []

    #get all information from database
    for info in information:
        product_name_list.append(info[3])
        price_list.append(info[4])
        date_list.append(info[1])
    
    #put all lists into a dictionary
    history = {}
    history["product"] = product_name_list
    history["price"] = price_list
    history["date"] = date_list

    return render_template("history.html", history=history, num_history=len(information))
    

@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    if request.method == "GET":
        return render_template("add_product.html")
    else:
        product_name = request.form.get('product_name')
        url_input = request.form.get('url')
        if not product_name or not url_input:
            return redirect("/apology")

        #insert information into database
        con = lite.connect("information.db")
        cur = con.cursor()
        cur.execute("INSERT INTO information (username, product_name, URL) VALUES (?, ?, ?)", (username_global, product_name, url_input))
        con.commit()
        con.close()

        return redirect("/")


@app.route("/add_history")
def add_to_history():
    add_history()
    return render_template("add_history.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


@app.route("/apology")
def apology():
    return render_template("apology.html")        

if __name__ == "__main__":
    app.run()