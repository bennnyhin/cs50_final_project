import bs4, sys
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import sqlite3 as lite

# initiate the database to be accessed
# con = lite.connect(database)
# with con:
#     cur = con.cursor()

def main():
    page_soup = find_html("https://www.lenovo.com/ca/en/laptops/thinkpad/thinkpad-x1/X1-Yoga-Gen-5/p/22TP2X1X1Y5")
    print(find_web_price(page_soup))
    print(find_sale_price(page_soup))
    print(find_processor_info(page_soup))


# use BeatifulSoup to get the html of the page
def find_html(my_url):
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")
    return page_soup


# create a list of the prices of the product before discount
def find_web_price(page_soup):
    containers = page_soup.findAll("div", {"class": "tabbedBrowse-productListing"})
    container = containers[0]
    web_price_list = []
    for container in containers:
        price_container = container.findAll("dd", {"class": "saleprice pricingSummary-priceList-value ls-has-discount"})
        web_price = price_container[0].text
        web_price_list.append(web_price)
    return web_price_list


# create a list of the prices of the products after discount
def find_sale_price(page_soup):
    containers = page_soup.findAll("div", {"class": "tabbedBrowse-productListing"})
    container = containers[0]
    sale_price_list = []
    for container in containers:
        price_container = container.findAll("dd", {"class": "saleprice pricingSummary-details-final-price"})
        sale_price = price_container[0].text
        sale_price_list.append(sale_price)
    return sale_price_list


#create a list of the processor information
def find_processor_info(page_soup):
    containers = page_soup.findAll("div", {"class": "tabbedBrowse-productListing-featureList featureList-bulleted featureList-linedRows"})
    container = containers[0]
    print (len(containers))
    print(container.dl.dd.text)
    processor_list = []
    for container in containers:
        processor_name = container.dl.dd.text
        processor_list.append(processor_name)
    return processor_list
    

if __name__ == "__main__":
    main()