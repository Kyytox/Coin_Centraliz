import datetime
import psycopg2
from dateutil import parser
from bs4 import BeautifulSoup
import requests
from twitchAPI.twitch import Twitch
import warnings
warnings.filterwarnings('ignore')


print("Lancement script TWITCH")

try:
    conn = psycopg2.connect(
        user="postgres",
        password='Caillault.012379',
        host="localhost",
        port="5432",
        database="coincentraliz"
    )
    cur = conn.cursor()
    sql_site_twitch = "SELECT title FROM news_site WHERE title = %s AND type = 'Twitch'"

    # Twitch
    # connect to twitch and collect all fr streamer online in category Crypto
    twitch = Twitch(
        '1paxqmgze600do5zd5hbm9yv3rxfvs', '72ybpbsy6xffrtvb16t4rc16xrkrnl')
    req = twitch.get_streams(game_id=['499634'], language=['fr'])
    # print(SoupStrainer.search_tag(markupName=user_name, markupAttrs={}))
    list_steamers = req['data']
    for streamer in list_steamers:
        user_name = streamer['user_name']

        # vérif if user exists in table site
        cur.execute(sql_site_twitch, (user_name,))
        result_sql_verif_twitch = cur.fetchone()

        if result_sql_verif_twitch is not None:
            print('continu')
            continue

        req_user = twitch.get_users(logins=[user_name])
        list_infos_user = req_user['data']
        for user in list_infos_user:
            thumbnail_url = user['profile_image_url']
            description = user['description']
            sql_insert_streamer = "INSERT INTO news_site (title, url, url_site, description, thumbnail, type) VALUES(%s,%s,%s,%s,%s,%s)"
            # execute the INSERT statement
            val_at_insert = (
                user_name, '.', f"https://www.twitch.tv/{user_name}", description, thumbnail_url, 'Twitch')

            print("insert BD")
            cur.execute(sql_insert_streamer, val_at_insert)

    # commit the changes to the database
    conn.commit()

    # fermeture de la connexion à la base de données
    cur.close()
    conn.close()
    print("La connexion PostgreSQL est fermée")
except (Exception, psycopg2.Error) as error:
    print("Erreur lors de la connexion à PostgreSQL", error)
