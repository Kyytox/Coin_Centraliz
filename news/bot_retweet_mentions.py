import tweepy
import time
from pprint import pprint
import psycopg2

# Initialization
auth = tweepy.OAuthHandler("",
                           "")
auth.set_access_token("-",
                      "")
api = tweepy.API(auth)

# Getting Bot ID
bot_id = int(api.verify_credentials().id_str)
# bot_id = 24246712

mention_id = 1

try:
    conn = psycopg2.connect(
        user="postgres",
        password='',
        host="localhost",
        port="5432",
        database="coincentraliz"
    )
    cur = conn.cursor()
    sql_tweets = "SELECT title FROM news_tweet WHERE title = %s"

    # Retweet Bot with Mentions
    while True:
        mentions = api.mentions_timeline(since_id=mention_id)

        for mention in mentions:
            print("Mention Tweet found!")
            print(f"MENTION: {mention.author.screen_name} - {mention.text}")
            mention_id = mention.id
            print("mention.id :", mention.id)
            print("mention.in_reply_to_status_id: ",
                  mention.in_reply_to_status_id)
            if mention.author.id != bot_id:
                try:
                    print("trying retweet...")
                    if mention.in_reply_to_status_id is None:
                        api.retweet(mention.id)
                        tweet = api.get_status(mention.id)
                        title_tweet = tweet.text
                        author_tweet = tweet.user.name
                        datepubli_tweet = tweet.created_at
                        url_tweet = f"https://twitter.com/{author_tweet}/status/{mention.id}"

                    else:
                        api.retweet(mention.in_reply_to_status_id)
                        tweet = api.get_status(mention.in_reply_to_status_id)
                        title_tweet = tweet.text
                        author_tweet = tweet.user.name
                        datepubli_tweet = tweet.created_at
                        url_tweet = f"https://twitter.com/{author_tweet}/status/{mention.in_reply_to_status_id}"

                    cur.execute(sql_tweets, (title_tweet,))
                    result_sql_verif_tweet = cur.fetchone()

                    if result_sql_verif_tweet is not None:
                        print('continue')
                        continue

                    sql_insert_tweet = "INSERT INTO news_tweet (title,author,datepubli,url) VALUES(%s,%s,%s,%s)"
                    # execute the INSERT statement
                    val_at_insert = (
                        title_tweet, author_tweet, datepubli_tweet, url_tweet)
                    cur.execute(sql_insert_tweet, val_at_insert)

                    print("Tweet successfully retweeted!\n")
                except Exception as err:
                    print(err)
                    print("Tweet will not be retweeted.\n")
        # commit the changes to the database
        conn.commit()

        # fermeture de la connexion à la base de données
        cur.close()
        conn.close()
        print("La connexion PostgreSQL est fermée")
except (Exception, psycopg2.Error) as error:
    print("Erreur lors de la connexion à PostgreSQL", error)
