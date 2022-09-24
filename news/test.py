from twitchAPI.twitch import Twitch
from pprint import pprint
import requests
from bs4 import BeautifulSoup
from unicodedata import category
from dateutil import parser
import warnings
import datetime
warnings.filterwarnings('ignore')

# Twitch
# connect to twitch and collect all fr streamer online in category Crypto
list_stream_online = []
twitch = Twitch('1paxqmgze600do5zd5hbm9yv3rxfvs',
                '72ybpbsy6xffrtvb16t4rc16xrkrnl')
req = twitch.get_streams(game_id=['499634'], language=['fr'])
list_infos_streams = req['data']
for stream in list_infos_streams:
    user_name = stream['user_name']
    title = stream['title']
    print('user_name: ', user_name)
    req_user = twitch.get_users(logins=[user_name])
    list_infos_user = req_user['data']
    for user in list_infos_user:
        thumbnail_url = user['profile_image_url']
        print('thumbnail_url: ', thumbnail_url)

        list_stream_online.append([user_name, title, thumbnail_url])

# twitch = Twitch(
#     '1paxqmgze600do5zd5hbm9yv3rxfvs', '72ybpbsy6xffrtvb16t4rc16xrkrnl')
# req = twitch.get_streams(game_id=['499634'], language=['fr'])
# # print(SoupStrainer.search_tag(markupName=user_name, markupAttrs={}))
# test = req['data']
# print("test: ", test[0]['user_name'])


# id = '1paxqmgze600do5zd5hbm9yv3rxfvs'
# secret = '72ybpbsy6xffrtvb16t4rc16xrkrnl'


# print("Lancement script Site Web")

# xml_data = requests.get('https://www.coinalist.io/feed/').content
# soup = BeautifulSoup(xml_data, "html.parser")
# print('soup: ', soup)


# # collect all tags "item"
# items = soup.find_all('item')
# print('items: ', items)

# # loops all tags "items" and collect title; guid(url); description; date publication
# for i in items:
#     # title
#     title_article = i.title.text

#     # verif if title as 'Graphiques Floor price', if true pass next i
#     if site_article == 'CoinAcademy' and ('Graphiques Floor price' or 'graphiques et prédiction') in title_article:
#         continue

#     # verif if article exist in Article table
#     cur.execute(sql_verif_article, (title_article,))
#     result_sql_verif_article = cur.fetchone()

#     if result_sql_verif_article is not None:
#         print('breakbreak')
#         break

#     # author
#     author_article = '' if site_article == 'CryptoNews' else i.find(
#         'dc:creator').text

#     # URL and Description
#     url_article = i.guid.text
#     description_article_convert = i.description.text
#     description_article = BeautifulSoup(
#         description_article_convert, "html.parser")

#     # date publication
#     datepubli_article = i.pubdate.text
#     datepubli_article = datepubli_article[:-5]
#     date_publi_article = parser.parse(datepubli_article)
#     time_change = datetime.timedelta(hours=4)
#     date_publi_article = date_publi_article + time_change

#     # Category
#     category_1 = ''
#     category_2 = ''
#     category_3 = ''
#     category_4 = ''
#     str_category_article = ''
#     tab_category = i.find_all('category')

#     for x in tab_category:
#         # create string wuth values of tab_category
#         str_category_article = f'{str_category_article}{x.text}, '

#     # loops all list category
#     for category in list_category:

#         isMatch = [
#             True for x in category if x in str_category_article[:-2]]
#         if True in isMatch:
#             name_category = category[0]

#             if category_1 == '' and name_category not in category_1:
#                 category_1 = name_category
#             elif category_2 == '' and name_category not in category_2:
#                 category_2 = name_category
#             elif category_3 == '' and name_category not in category_3:
#                 category_3 = name_category
#             elif category_4 == '' and name_category not in category_4:
#                 category_4 = name_category
