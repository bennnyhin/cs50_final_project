import bs4, sys
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import sqlite3 as lite
import scrape

initiate the database to be accessed
con = lite.connect("information.db")
cur = con.cursor()

def main():
    page_soup = scrape.find_html("https://www.lenovo.com/ca/en/laptops/thinkpad/thinkpad-x1/X1-Yoga-Gen-5/p/22TP2X1X1Y5")
    print(scrape.find_web_price(page_soup))
    print(scrape.find_sale_price(page_soup))
    print(scrape.find_processor_info(page_soup))
    # cur.execute("INSERT INTO users (username, password) VALUES ('ben', 'blah')")

    con.commit()
    con.close()
    

if __name__ == "__main__":
    main()