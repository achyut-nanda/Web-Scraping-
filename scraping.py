import pandas as pd
from bs4 import BeautifulSoup
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}
productNames = []
productPrices = []
productRatings = []
url = "https://www.flipkart.com/search?q=mobile+phones+under+50000&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page="

# Get the total number of pages
firstPageUrl = "https://www.flipkart.com/search?q=mobile+phones+under+50000&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=1"
response = requests.get(firstPageUrl, headers=headers)
soup = BeautifulSoup(response.text, "lxml")
try:
    pagination_text = soup.find('div', {'class': 'FF6GgS'}).find('span').text
    totalPages = int(pagination_text.split("of")[-1].strip().replace(',', ''))
except AttributeError:
    totalPages = 1

print(f"Total Pages Found: {totalPages}")

# Start scraping data from all pages
for i in range(1,totalPages + 1):
    completeUrl = url + str(i)
    r = requests.get(completeUrl)
    soup = BeautifulSoup(r.text, "lxml")
    box = soup.find("div", class_="QSCKDh dLgFEE")
    
    names = box.find_all("div", class_="RG5Slk")
    for i in names:
        name = i.text
        productNames.append(name)
    
    prices = box.find_all("div", class_="hZ3P6w DeU9vF")
    for i in prices:
        price = i.text
        productPrices.append(price)

    ratings = box.find_all("div", class_="MKiFS6")
    for i in ratings:
        rating = i.text
        productRatings.append(rating)

dataFrame = pd.DataFrame({
    "Product Name": productNames,
    "Product Price": productPrices,
    "Product Rating": productRatings
})
dataFrame.to_csv("mobile_phones_under_50000.csv")