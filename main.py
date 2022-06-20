import pandas
from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd

response = requests.get('https://www.abenson.com/mobile/smartphone.html')
phones = response.text
soup = BeautifulSoup(phones, 'html.parser')
titles = soup.find_all(name='a', class_='product-item-link')
phone_list = []
for title in titles:
    title = title.getText()
    title = title.strip()
    title = title.strip('\n')
    phone_list.append(title)
desc_list = []
desc = soup.find_all(name='div', class_='product-item-inner')
for des in desc:
    des = des.getText()
    des = des.strip()
    des = des.strip('\n')
    desc_list.append(des)
# print(desc_list)
new_price_list = []
new_price_int = []
old_price_list = []
disc_list = []
monthly_list = []
prices = soup.find_all(name='div', class_='price-box')
for price in prices:
    price = price.getText()
    price = price.split()
    if len(price) > 2:
        new_price_list.append(price[0])
        price[0] = price[0].strip('₱')
        price[0] = price[0].split(',')
        price[0] = price[0][0] + price[0][1]
        new_price_int.append(int(price[0]))
        old_price_list.append(price[1])
        disc_list.append(price[2])
        monthly_list.append(price[3])
    else:
        new_price_list.append(price[0])
        price[0] = price[0].strip('₱')
        price[0] = price[0].split(',')
        price[0] = price[0][0] + price[0][1]
        new_price_int.append(int(price[0]))
        old_price_list.append("")
        disc_list.append("")
        monthly_list.append(price[1])

dict = {'Phone Model': phone_list, 'Specifications' : desc_list, 'New Price' : new_price_list, 'Discount': disc_list,
        'Regular Price' : old_price_list, 'Monthly' : monthly_list, 'Price Int': new_price_int }
df = pd.DataFrame(dict)
df.to_csv('phone_prices.csv')

data = pandas.read_csv('phone_prices.csv')
data_dict = data.to_dict()
print('Item#','Phone Model','Specifications','Price')
for i in range(1,len(data_dict['Phone Model'])+1):
    print(i,data_dict['Phone Model'][i-1], data_dict['Specifications'][i-1],data_dict['New Price'][i-1])