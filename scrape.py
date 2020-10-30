import bs4, sys
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

# use BeatifulSoup to get the html of the page
def find_html(my_url):
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")
    return page_soup


# get the price of the base model before discount
def find_web_price(page_soup, number):
    containers = page_soup.findAll("div", {"class": "tabbedBrowse-productListing"})
    container = containers[number]
    price_container = container.findAll("dd", {"class": "saleprice pricingSummary-priceList-value ls-has-discount"})
    web_price = price_container[0].text
    return web_price.strip()


# create a list of the prices of the products after discount
def find_sale_price(page_soup, number):
    containers = page_soup.findAll("div", {"class": "tabbedBrowse-productListing"})
    container = containers[number]
    price_container = container.findAll("dd", {"class": "saleprice pricingSummary-details-final-price"})
    sale_price = price_container[0].text
    return sale_price.strip()


#create a list of the processor information
def find_processor_info(page_soup, number):
    containers = page_soup.findAll("div", {"class": "tabbedBrowse-productListing-featureList featureList-bulleted featureList-linedRows"})
    container = containers[number]
    processor_name = container.dl.dd.text
    return processor_name.strip()

def find_base_model(page_soup):
    containers = page_soup.findAll("div", {"class": "tabbedBrowse-productListing-merchandising-label"})
    counter = 0
    for container in containers:
        name = container.div.text
        if name == "Build your own":
            return counter
        counter += 1
    return


