import requests
from bs4 import BeautifulSoup
from unicodedata import category
from dateutil import parser
import warnings
import psycopg2
import datetime
warnings.filterwarnings('ignore')

print("Lancement script Site Web")


# variables
myList_BTC = ['BTC', 'Bitcoin',
              'Actualités Bitcoin', 'Lightning', 'bitcoin']
myList_ETH = ['ETH', 'Ethereum',
              '(ETH)', 'Actualités Ethereum', 'Proof-of-stake']
myList_Altcoins = ['Altcoins', 'Cryptos', 'USDT', 'Arbitrum', 'Stablecoin', 'Terra', 'SOL', 'layer 2', 'Polygon', 'rollups', 'Avalanche', 'AVAX', 'Monero', 'XMR', 'ALT', 'Actualité des Altcoins',
                   'altcoins', 'Polkadot', 'Cryptomonnaies & Altcoins', 'Ethereum', 'ETH', '(ETH)', 'Actualité Ethereum', 'Dogecoin', 'Crypto', 'Cryptomonnaies', 'LUNA', 'UST', 'BNB', 'ATOM', 'Aave']
myList_DEFI = ['DEFI', 'décentralisée', 'DeFi', 'Defi']
myList_NFT = ['NFT', 'Gaming', 'Métavers', 'Metaverse',
              'Collectibles', 'non Fongible', 'non fongibles', 'NFTs']
myList_Gaming = ['Gaming', 'Play2earn']
myList_Blockchain = ['Blockchain', 'la Blockchain',
                     'layer 2', 'Web 3.0', 'Web 3', 'web 3']
myList_Exchange = ['Exchange', 'Exchanges',
                   'Coinbase', 'DEX',  'Binance', 'FTX']
myList_Trading = ['Trading', 'Analyse',
                  'Analyses', 'analyse', 'trading', 'courbes', ]
myList_Marche = ['Marchés', 'Canada', 'Adoption', 'USA', 'Régulation', 'SEC', 'Opinions',
                 'Legal', 'CBDC', 'Banque', 'Banques', 'Chine', 'Economie', 'MNBC', 'Institutionnel']
myList_Metaverse = ['Métavers', 'Metaverse', 'Méta', 'Collectibles']
myList_Securite = ['Sécurité', 'Piratage',
                   'Confidentialité', 'anonymat', 'Hack', 'Faille']

list_category = [myList_BTC, myList_ETH, myList_Altcoins, myList_DEFI, myList_NFT, myList_Gaming,
                 myList_Blockchain, myList_Exchange, myList_Trading, myList_Marche, myList_Metaverse, myList_Securite]


try:
    conn = psycopg2.connect(
        user="postgres",
        password='Caillault.012379',
        host="localhost",
        port="5432",
        database="coincentraliz"
    )
    cur = conn.cursor()

    sql_site_article = "SELECT title FROM news_site WHERE url = %s"
    sql_verif_article = "SELECT title FROM news_article WHERE title = %s"
    sql_article_url = "SELECT url FROM news_site WHERE type = 'Article'"
    cur.execute(sql_article_url)

    for url in cur.fetchall():
        print('x: ', url[0])
        xml_data = requests.get(url[0]).content
        soup = BeautifulSoup(xml_data, "html.parser")

        # site of article collect in table Site
        cur.execute(sql_site_article, (url[0],))
        result_sql_site_article = cur.fetchone()
        if result_sql_site_article is None:
            continue
        else:
            site_article = result_sql_site_article[0]

        # collect all tags "item"
        items = soup.find_all('item')

        # loops all tags "items" and collect title; guid(url); description; date publication
        for i in items:
            # title
            title_article = i.title.text

            # verif if title as 'Graphiques Floor price', if true pass next i
            if site_article == 'CoinAcademy' and ('Graphiques Floor price' or 'graphiques et prédiction') in title_article:
                continue

            # verif if article exist in Article table
            cur.execute(sql_verif_article, (title_article,))
            result_sql_verif_article = cur.fetchone()

            if result_sql_verif_article is not None:
                print('breakbreak')
                break

            # author
            author_article = '' if site_article == 'CryptoNews' else i.find(
                'dc:creator').text

            # URL and Description
            url_article = i.guid.text
            description_article_convert = i.description.text
            description_article = BeautifulSoup(
                description_article_convert, "html.parser")

            # date publication
            datepubli_article = i.pubdate.text
            datepubli_article = datepubli_article[:-5]
            date_publi_article = parser.parse(datepubli_article)
            time_change = datetime.timedelta(hours=2)
            date_publi_article = date_publi_article + time_change

            # Category
            category_1 = ''
            category_2 = ''
            category_3 = ''
            category_4 = ''
            str_category_article = ''
            tab_category = i.find_all('category')

            for x in tab_category:
                # create string wuth values of tab_category
                str_category_article = f'{str_category_article}{x.text}, '

            # loops all list category
            for category in list_category:

                isMatch = [
                    True for x in category if x in str_category_article[:-2]]
                if True in isMatch:
                    name_category = category[0]

                    if category_1 == '' and name_category not in category_1:
                        category_1 = name_category
                    elif category_2 == '' and name_category not in category_2:
                        category_2 = name_category
                    elif category_3 == '' and name_category not in category_3:
                        category_3 = name_category
                    elif category_4 == '' and name_category not in category_4:
                        category_4 = name_category

            sql_insert_article = "INSERT INTO news_article (title,author,datepubli,description,category_1,category_2,category_3,category_4,category_environnement,url,site) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            # execute the INSERT statement
            val_at_insert = (title_article, author_article, date_publi_article, description_article.text,
                             category_1, category_2, category_3, category_4, False, url_article, site_article)

            cur.execute(sql_insert_article, val_at_insert)

            # commit the changes to the database
            conn.commit()

    # fermeture de la connexion à la base de données
    cur.close()
    conn.close()
    print("La connexion PostgreSQL est fermée")
except (Exception, psycopg2.Error) as error:
    print("Erreur lors de la connexion à PostgreSQL", error)
