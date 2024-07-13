import requests
from bs4 import BeautifulSoup
import re

link = 'https://www.subito.it/annunci-italia/vendita/telefonia/?q=iphone&qso=true&shp=true&order=datedesc&advt=0&pht=1'
page = requests.get(link)
soup = BeautifulSoup(page.text, 'html.parser')

product_list_items = soup.find_all('div', class_=re.compile(r'item-card'))

for item in product_list_items:
    a_tag = item.find('a', class_='SmallCard-module_link__hOkzY')
    href = a_tag['href'] if a_tag else 'N/A'
    
    price_tag = item.find('p', class_='index-module_price__N7M2x')
    price = price_tag.text.strip() if price_tag else 'N/A'
    price = price.replace('.', '')
    price = price.replace(',', ' ')
    price = int(price.split('€')[0])
    
    print('URL:', href)
    print('Prezzo:', price)
    print('---')