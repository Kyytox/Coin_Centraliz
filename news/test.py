# Importing all modules/packages/libraries
# import tweepy
# import time

# # Initialization
# auth = tweepy.OAuthHandler("jedI81cVNadFucrO8awVbzWcp",
#                            "z8osPI7E3y4PdmMTva6Uwos2grdcl1bYY2GXHH12GV4qQF7F34")
# auth.set_access_token("1524521336420380672-EB8tdVauKSm0k7dYoqMYeaNtzgjeju",
#                       "BqVdF5VMZInN0s75H0Aelsu0liaIfRJZU1ESzlFmieViQ")
# api = tweepy.API(auth)

# # Getting Bot ID
# bot_id = int(api.verify_credentials().id_str)
# # bot_id = 24246712

# mention_id = 1

# # Retweet Bot with Mentions
# while True:
#     mentions = api.mentions_timeline(since_id=mention_id)
#     for mention in mentions:
#         print("Mention Tweet found!")
#         print(f"MENTION: {mention.author.screen_name} - {mention.text}")
#         mention_id = mention.id
#         if mention.in_reply_to_status_id is None and mention.author.id != bot_id:
#             try:
#                 print("trying retweet...")
#                 api.retweet(mention.id)
#                 print("Tweet successfully retweeted!\n")
#             except Exception as err:
#                 print(err)
#                 print("Tweet will not be retweeted.\n")
#     time.sleep(15)


# import requests
# from bs4 import BeautifulSoup
# from unicodedata import category
# from dateutil import parser
# import warnings
# import psycopg2
# import datetime
# warnings.filterwarnings('ignore')


# xml_data = requests.get('https://anchor.fm/s/8f4024c/podcast/rss').content
# # print('xml_data: ', xml_data)
# soup = BeautifulSoup(xml_data, "html.parser")

# # collect all tags "item"
# items = soup.find_all('item')

# print('items: ', items[0])

# # loops all tags "items" and collect title; guid(url); description; date publication
# for i in items:
#     # print('i: ', i)
#     # # title
#     title_article = i.title.text
#     print('title_article: ', title_article)

#     # author_media = i.author.find('name').text
#     # print('author_media: ', author_media)

#     datepubli_media = i.pubdate
#     print('datepubli_media: ', datepubli_media)

#     url_media = i.link.text
#     print('url_media: ', url_media)

# # image_media = i.find('media:thumbnail')['url']
# # print('image_:media: ', image_media)

# # verif if title as 'Graphiques Floor price', if true pass next i
# # if ('Graphiques Floor price' or 'graphiques et prédiction') not in title_article:
