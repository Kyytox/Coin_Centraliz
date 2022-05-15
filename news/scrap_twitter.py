
from turtle import title
import snscrape.modules.twitter as sntwitter
import psycopg2


try:
    conn = psycopg2.connect(
        user="postgres",
        password='Caillault.012379',
        host="localhost",
        port="5432",
        database="coincentraliz"
    )
    cur = conn.cursor()

    # Using TwitterSearchScraper to scrape x records from username @jack
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper('from:CoinCentraliz include:nativeretweets').get_items()):
        if i >= 2:
            break

        # recupr des 25 premiers caracteres
        tweet_user = tweet.content[:25]

        # on cherche la position da @
        pos1 = tweet_user.find('@')

        # on cherche la position de :
        pos2 = tweet_user.find(':')

        # extraction du nom de l'utilisateur sans l'@
        sousChaine_user = tweet_user[pos1+1:pos2]
        print('sousChaine_user : ', sousChaine_user)

        # on recup une chaine de caractere pour pouvoir retrouver le tweet sur le compte de l'user récup plus tot
        tweet_search = tweet.content[25:50]
        print('tweet_search : ', tweet_search)

        # Using TwitterSearchScraper to scrape x records from username in sousChaine_user
        for n, tweet in enumerate(sntwitter.TwitterSearchScraper(f'from:{sousChaine_user}').get_items()):
            if n > 200:
                break

            # on va cherche un tweet contenant tweet_1search et on recup ces infos
            if tweet_search in tweet.content:
                print(tweet.id, tweet.date, tweet.url,
                      tweet.username, tweet.content)

                title_tweet = tweet.content
                author_tweet = tweet.user.username
                datepubli_tweet = tweet.date
                url_tweet = tweet.url

                print('title_tweet: ', title_tweet)
                print('author_tweet: ', author_tweet)
                print('datepubli_tweet: ', datepubli_tweet)
                print('url_tweet: ', url_tweet)

                sql_insert_tweet = "INSERT INTO news_tweet (title,author,datepubli,url) VALUES(%s,%s,%s,%s)"
                # execute the INSERT statement
                val_at_insert = (title_tweet, author_tweet,
                                 datepubli_tweet, url_tweet)

                cur.execute(sql_insert_tweet, val_at_insert)
                # commit the changes to the database
                conn.commit()

                # fermeture de la connexion à la base de données
                cur.close()
                conn.close()
                print("La connexion PostgreSQL est fermée")
except (Exception, psycopg2.Error) as error:
    print("Erreur lors de la connexion à PostgreSQL", error)
