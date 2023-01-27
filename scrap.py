import requests
from bs4 import BeautifulSoup
import pandas as pd
# To get user agent -> https://httpbin.org/get
headers = {
    'User-Agent': 'ozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}
# We Will Scrap Best Selling Product from amazon.com
url = 'https://www.amazon.com/Best-Sellers-Electronics-Projection-Lamps/zgbs/electronics/3349991/ref=zg_bs_nav_electronics_4_14213579011' #'https://www.amazon.in/s?k=samsung'

def get_page_source(url):
    response = requests.get(url, headers=headers)
    print('#get data from amazon')
    return response.content

# To get product title
def get_title(soup):
    try:
        product_name = soup.find_all('a',{'class':'a-link-normal','role':'link'})[1].text
    except AttributeError:
        product_name = ''
    return product_name

# To get Product rating
def get_rating(result):
    try:
        rating = result.find('i', {'class': 'a-icon'}).text
        rating_count = result.find('span', class_='a-size-small').text
    except AttributeError:
        rating = 0
        rating_count = 0
    return [rating,rating_count]

# To get Product Price
def get_price(soup):
    try:
        price = soup.find('span', class_='a-size-base').text
    except AttributeError:
        price = ''
    return price

# To get Product Detail Page URL
def get_url(soup):
    try:
        product_url = 'https://amazon.com' + soup.find('a',{'class':'a-link-normal','role':'link'})['href']
    except AttributeError:
        product_url = ''
    return product_url

# To get Product Image URL
def get_img(soup):
    try:
        img = soup.find('img')['src']
    except AttributeError:
        img = ''
    return img

htmlContent = get_page_source(url)
soup = BeautifulSoup(htmlContent, 'lxml')
#results = soup.find_all('div', {'class': 's-result-item', 'data-component-type': 's-search-result'})
results = soup.find_all('div', {'class': 'p13n-sc-uncoverable-faceout'})

items = [] # Hold the scraped product list 

for result in results:
    product_dict = {}
    rating_list = get_rating(result)
    product_dict['name'] = get_title(result)
    product_dict['rating'] = rating_list[0]
    product_dict['rating_count'] = rating_list[1]
    product_dict['price'] = get_price(result)
    product_dict['product_url'] = get_url(result)
    product_dict['product_img'] = get_img(result)
    items.append(product_dict)

# Write data into csv file
df = pd.DataFrame(items)
df.to_csv('amazon-products.csv',index=False)
