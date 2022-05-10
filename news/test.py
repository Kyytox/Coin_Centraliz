import requests
from bs4 import BeautifulSoup
from unicodedata import category
from dateutil import parser
import warnings
import psycopg2
import datetime
warnings.filterwarnings('ignore')


xml_data = requests.get('https://anchor.fm/s/8f4024c/podcast/rss').content
# print('xml_data: ', xml_data)
soup = BeautifulSoup(xml_data, "html.parser")

# collect all tags "item"
items = soup.find_all('item')

print('items: ', items[0])

# loops all tags "items" and collect title; guid(url); description; date publication
for i in items:
    # print('i: ', i)
    # # title
    title_article = i.title.text
    print('title_article: ', title_article)

    # author_media = i.author.find('name').text
    # print('author_media: ', author_media)

    datepubli_media = i.pubdate
    print('datepubli_media: ', datepubli_media)

    url_media = i.link.text
    print('url_media: ', url_media)

# image_media = i.find('media:thumbnail')['url']
# print('image_:media: ', image_media)

# verif if title as 'Graphiques Floor price', if true pass next i
# if ('Graphiques Floor price' or 'graphiques et prédiction') not in title_article:
