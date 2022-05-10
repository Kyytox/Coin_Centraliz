import requests
from bs4 import BeautifulSoup
from dateutil import parser
import psycopg2
import datetime


print("Lancement script YOUTUBE")

try:
    conn = psycopg2.connect(
        user="postgres",
        password='Caillault.012379',
        host="localhost",
        port="5432",
        database="coincentraliz"
    )
    cur = conn.cursor()

    sql_youtube_site = "SELECT title FROM news_site WHERE url = %s"
    sql_verif_media = "SELECT title FROM news_media WHERE title = %s"
    sql_media_url = "SELECT url FROM news_site WHERE type = 'Media' or type = 'Trading'"
    cur.execute(sql_media_url)

    for url in cur.fetchall():
        print('x: ', url[0])
        xml_data = requests.get(url[0]).content
        soup = BeautifulSoup(xml_data, "html.parser")

        # site of article collect in table Site
        cur.execute(sql_youtube_site, (url[0],))
        result_sql_youtube_media = cur.fetchone()
        if result_sql_youtube_media is None:
            continue
        else:
            author_media = result_sql_youtube_media[0]

        # collect all tags "entry"
        items = soup.find_all('entry')

        # loops all tags "items" and collect title; guid(url); description; date publication
        for i in items:

            title_media = i.title.text

            cur.execute(sql_verif_media, (title_media,))
            result_sql_verif_media = cur.fetchone()

            if result_sql_verif_media is not None:
                print('result_sql_verif_article: ', result_sql_verif_media)
                print('breakbreak')
                break

            author_media = i.author.find('name').text

            datepubli_media = i.published.text
            datepubli_media = datepubli_media[:-6]
            date_publi_media = parser.parse(datepubli_media)
            time_change = datetime.timedelta(hours=2)
            date_publi_media = date_publi_media + time_change

            # description_media = i.find('media:description').text

            url_media = i.link['href']
            image_media = i.find('media:thumbnail')['url']

            sql_insert_media = "INSERT INTO news_media (title, author, datepubli, url, category_environnement, thumbnail) VALUES(%s,%s,%s,%s,%s,%s)"
            # execute the INSERT statement
            val_at_insert = (title_media, author_media,
                             date_publi_media, url_media, False, image_media)

            cur.execute(sql_insert_media, val_at_insert)

            # commit the changes to the database
            conn.commit()

    # fermeture de la connexion à la base de données
    cur.close()
    conn.close()
    print("La connexion PostgreSQL est fermée")
except (Exception, psycopg2.Error) as error:
    print("Erreur lors de la connexion à PostgreSQL", error)
