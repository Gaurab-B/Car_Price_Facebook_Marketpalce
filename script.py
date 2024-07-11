import pandas as pd
import numpy as np
import re
from bs4 import BeautifulSoup
from datetime import datetime

locationa = input("Which location are you scraping cars for?")

def removal(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
        content = f" {content} "
        content = content.replace("'", "")
    return content

path = "temp.txt"
content = removal(path) # update the current file
with open(path, 'w', encoding='utf-8') as file:
    file.write(content)  # write the updated content back to the file

with open(path, 'r', encoding='utf-8') as file:
    file_contents = file.read()  # read the updated file

data = file_contents #data has all the html code necessary
soup = BeautifulSoup(data, 'html.parser')

link_div = soup.find_all('div', class_="x3ct3a4")
links = []
for car_element in link_div:
    link_tag = car_element.find('a', class_='x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1sur9pj xkrqix3 x1lku1pv')
    link = link_tag['href'] if link_tag else None
    links.append(link)
all_div = soup.find_all('div', class_="x9f619 x78zum5 xdt5ytf x1qughib x1rdy4ex xz9dl7a xsag5q8 xh8yej3 xp0eagm x1nrcals")
models = []
price = []
locations = []
miles = []


# Iterate through each car element
for car_element in all_div:
    
    price_span = car_element.find('span', class_='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x676frb x1lkfr7t x1lbecb7 x1s688f xzsf02u')
    model_price = price_span.get_text(strip=True) if price_span else None
    price.append(model_price)
    
    # Extract model name
    model_span = car_element.find('span', class_='x1lliihq x6ikm8r x10wlt62 x1n2onr6')
    model_name = model_span.get_text(strip=True) if model_span else None
    models.append(model_name)

    # Find the spans inside the current car element
    all_spans = car_element.find_all('span', class_='x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1j85h84')

    # Extract location and miles
    if len(all_spans) > 1:
        location_span = all_spans[0]
        location = location_span.get_text(strip=True)
        locations.append(location)

        miles_span = all_spans[1]
        miles_text = miles_span.get_text(strip=True)
        miles.append(miles_text)
    else:
        locations.append(None)
        miles.append(None)
df = pd.DataFrame({
    'Model': models,
    'Location': locations,
    'Miles': miles,
    'Prices': price,
    'Link': links
})
df = df.dropna(subset=['Location'])
df['Model'] = df['Model'].astype(str)
df['Year'] = df['Model'].str.extract(r'(\d{4})')
df['Model'] = df['Model'].str[4:]
df['Scraped_On'] = datetime.today().strftime('%Y-%m-%d')
df['Link'] = df['Link'].astype(str)
df['Link'] = 'https://www.facebook.com/' + df['Link']
new_order = ['Model', 'Year', 'Miles', 'Location' , 'Prices', 'Link', 'Scraped_On']
df = df[new_order]
dd = datetime.today().strftime('%Y-%m-%d')
output_Text = dd + "-" + locationa + ".csv"
df.to_csv(output_Text, index=False)

print("DataFrame saved!")

