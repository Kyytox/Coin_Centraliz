import psycopg2


print("Lancement insert BD")


list_site_ajout = [['CryptoNews', 'https://fr.cryptonews.com/', 'https://fr.cryptonews.com/news/feed/', 'Article'],
                   ['Journal du coin', 'https://journalducoin.com/',
                       'https://journalducoin.com/feed/', 'Article'],
                   ['CryptToast', 'https://cryptoast.fr/',
                       'https://cryptoast.fr/feed/', 'Article'],
                   ['CoinAcademy', 'https://coinacademy.fr/',
                       'https://coinacademy.fr/feed/', 'Article'],
                   ['Bitcoin.fr', 'https://bitcoin.fr/',
                       'https://bitcoin.fr/feed/', 'Article'],
                   ['Coins.fr', 'https://coins.fr/',
                       'https://coins.fr/feed/', 'Article'],
                   ['Cointribune', 'https://www.cointribune.com/',
                       'https://www.cointribune.com/feed/', 'Article'],
                   ['CryptoActu', 'https://cryptoactu.com/',
                       'https://cryptoactu.com/feed/', 'Article'],
                   ['Grand Angle Crypto', 'https://www.youtube.com/channel/UCT5FYQ_io06t7aY8rShgzvA',
                       'https://www.youtube.com/feeds/videos.xml?channel_id=UCT5FYQ_io06t7aY8rShgzvA', 'Media'],
                   ['Découvre Bitcoin', 'https://www.youtube.com/channel/UCANjJ55UmYmoXm_SW--psXQ',
                       'https://www.youtube.com/feeds/videos.xml?channel_id=UCANjJ55UmYmoXm_SW--psXQ', 'Media'],
                   ["Surfin' Bitcoin", 'https://www.youtube.com/channel/UChfepkLjWJzSW16QArGYxWg',
                       'https://www.youtube.com/feeds/videos.xml?channel_id=UChfepkLjWJzSW16QArGYxWg', 'Media'],
                   ['Univers Bitcoin Podcast', 'https://www.youtube.com/channel/UCOlhr_6OnEnqV8wrbrnLZvQ',
                       'https://www.youtube.com/feeds/videos.xml?channel_id=UCOlhr_6OnEnqV8wrbrnLZvQ', 'Media'],
                   ['Parlons Bitcoin', 'https://www.youtube.com/channel/UCBLCX3V2DeoP1wrEfxG-z0g',
                       'https://www.youtube.com/feeds/videos.xml?channel_id=UCBLCX3V2DeoP1wrEfxG-z0g', 'Media'],
                   ["Parlons Crypto - L'émission", 'https://www.youtube.com/channel/UCx3KJIw43_1q4gKpJkiaRJg',
                       'https://www.youtube.com/feeds/videos.xml?channel_id=UCx3KJIw43_1q4gKpJkiaRJg', 'Media'],
                   ['Journal du Coin', 'https://www.youtube.com/channel/UC7qnB0XxzOEwWWn9Q6HPmCw',
                       'https://www.youtube.com/feeds/videos.xml?channel_id=UC7qnB0XxzOEwWWn9Q6HPmCw', 'Media'],
                   ['Cryptoast', 'https://www.youtube.com/channel/UCD9yJ3yOv6hCMeYLYAVi7zw',
                       'https://www.youtube.com/feeds/videos.xml?channel_id=UCD9yJ3yOv6hCMeYLYAVi7zw', 'Media'],
                   ['Hasheur', 'https://www.youtube.com/channel/UChlTcWDE8gd4tsl_L727NrQ',
                       'https://www.youtube.com/feeds/videos.xml?channel_id=UChlTcWDE8gd4tsl_L727NrQ', 'Media'],
                   ['Crypto Farmeur', 'https://www.youtube.com/channel/UCJQ5j2qqWWOj800lCrsb34g',
                       'https://www.youtube.com/feeds/videos.xml?channel_id=UCJQ5j2qqWWOj800lCrsb34g', 'Media'],
                   ['Crok - Crypto News', 'https://www.youtube.com/channel/UCOJzqoA84sSqdfkF5hw3Uyg',
                       'https://www.youtube.com/feeds/videos.xml?channel_id=UCOJzqoA84sSqdfkF5hw3Uyg', 'Media'],
                   ['Monsieur-TK', 'https://www.youtube.com/channel/UC0DITweI6K01RpfrJDMQWFw',
                       'https://www.youtube.com/feeds/videos.xml?channel_id=UC0DITweI6K01RpfrJDMQWFw', 'Media'],
                   ['CryptoLogik', 'https://www.youtube.com/channel/UCU5xRfYU2CZHyoFwmHVFipw',
                       'https://www.youtube.com/feeds/videos.xml?channel_id=UCU5xRfYU2CZHyoFwmHVFipw', 'Media'],
                   ['fund3r community', 'https://www.youtube.com/channel/UCJwSVnTxXFOoR8E_iBPHbpw',
                       'https://www.youtube.com/feeds/videos.xml?channel_id=UCJwSVnTxXFOoR8E_iBPHbpw', 'Media'],
                   ['DeFi France', 'https://www.youtube.com/channel/UCztkHfSVCdriSpzvZF7Qwtg',
                       'https://www.youtube.com/feeds/videos.xml?channel_id=UCztkHfSVCdriSpzvZF7Qwtg', 'Media'],
                   ['Decryptalk', 'https://www.youtube.com/channel/UCi7NBlzOjoSgRcE7GQpRp6Q',
                       'https://www.youtube.com/feeds/videos.xml?channel_id=UCi7NBlzOjoSgRcE7GQpRp6Q', 'Media'],
                   ['Learn & Earn Crypto Podcast [Francophone]', 'https://www.youtube.com/channel/UCbnFckir-MItQ1uAWtZ4RNA',
                       'https://www.youtube.com/feeds/videos.xml?channel_id=UCbnFckir-MItQ1uAWtZ4RNA', 'Media'],
                   ['21 Millions', 'https://www.youtube.com/channel/UCVQ4B7feh8kCMwxL4ncX7UA',
                       'https://www.youtube.com/feeds/videos.xml?channel_id=UCVQ4B7feh8kCMwxL4ncX7UA', 'Media'],
                   ['Zap Crypto', 'https://www.youtube.com/channel/UCC6qHgCsdeePOHWHjSEF0uA',
                       'https://www.youtube.com/feeds/videos.xml?channel_id=UCC6qHgCsdeePOHWHjSEF0uA', 'Media'],
                   ['DANA', 'https://www.youtube.com/channel/UCqobh_KasBC1hUIluHGqtTA',
                       'https://www.youtube.com/feeds/videos.xml?channel_id=UCqobh_KasBC1hUIluHGqtTA', 'Media'],
                   ['Wave Trading France', 'https://www.youtube.com/channel/UCQN2wjWxpMdDeaz7_El1nxg',
                       'https://www.youtube.com/feeds/videos.xml?channel_id=UCQN2wjWxpMdDeaz7_El1nxg', 'Trading'],
                   ['Enter The Crypto Matrix', 'https://www.youtube.com/channel/UCefQC4Y-X9MBRuYBKc2waiQ',
                       'https://www.youtube.com/feeds/videos.xml?channel_id=UCefQC4Y-X9MBRuYBKc2waiQ', 'Media'],
                   ['Crypto Picsou', 'https://www.youtube.com/channel/UCZioDtSSkxEmeN0Iqv9neHA',
                       'https://www.youtube.com/feeds/videos.xml?channel_id=UCZioDtSSkxEmeN0Iqv9neHA', 'Media'],
                   ['Khalistas to the moon', 'https://www.youtube.com/channel/UCUE_Y-qamqLT-5bsihtCphw',
                       'https://www.youtube.com/feeds/videos.xml?channel_id=UCUE_Y-qamqLT-5bsihtCphw', 'Trading'],
                   ['Captain Trading', 'https://www.youtube.com/channel/UCJdx6xfJVFLXJuv9I7ECuRA', 'https://www.youtube.com/feeds/videos.xml?channel_id=UCJdx6xfJVFLXJuv9I7ECuRA', 'Trading']]


try:
    conn = psycopg2.connect(
        user="postgres",
        password='Caillault.012379',
        host="localhost",
        port="5432",
        database="coincentraliz"
    )
    cur = conn.cursor()

    for site in list_site_ajout:

        title = site[0],
        url = site[2],
        url_site = site[1],
        type_ = site[3]

        sql_insert_media = "INSERT INTO news_site (title, url, url_site, type) VALUES(%s,%s,%s,%s)"
        # execute the INSERT statement
        val_at_insert = (title, url,
                         url_site, type_)

        cur.execute(sql_insert_media, val_at_insert)

        # commit the changes to the database
        conn.commit()

    # fermeture de la connexion à la base de données
    cur.close()
    conn.close()
    print("La connexion PostgreSQL est fermée")
except (Exception, psycopg2.Error) as error:
    print("Erreur lors de la connexion à PostgreSQL", error)
