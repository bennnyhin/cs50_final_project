import bs4, sys
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = "https://www.lenovo.com/ca/en/laptops/thinkpad/thinkpad-x/X1-Yoga-Gen-5/p/22TP2X1X1Y5"

uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html,"html.parser")

containers = page_soup.findAll("div", {"class": "tabbedBrowse-productListing"})
container = containers[0]
price_container = container.findAll("dd", {"class": "saleprice pricingSummary-priceList-value ls-has-discount"})
price = price_container[0].text
print(price)



