import tweepy
import time

# Initialization
auth = tweepy.OAuthHandler("jedI81cVNadFucrO8awVbzWcp",
                           "z8osPI7E3y4PdmMTva6Uwos2grdcl1bYY2GXHH12GV4qQF7F34")
auth.set_access_token("1524521336420380672-EB8tdVauKSm0k7dYoqMYeaNtzgjeju",
                      "BqVdF5VMZInN0s75H0Aelsu0liaIfRJZU1ESzlFmieViQ")
api = tweepy.API(auth)

# Getting Bot ID
bot_id = int(api.verify_credentials().id_str)
# bot_id = 24246712

mention_id = 1

# Retweet Bot with Mentions
while True:
    mentions = api.mentions_timeline(since_id=mention_id)
    for mention in mentions:
        print("Mention Tweet found!")
        print(f"MENTION: {mention.author.screen_name} - {mention.text}")
        mention_id = mention.id
        if mention.in_reply_to_status_id is None and mention.author.id != bot_id:
            try:
                print("trying retweet...")
                api.retweet(mention.id)
                print("Tweet successfully retweeted!\n")
            except Exception as err:
                print(err)
                print("Tweet will not be retweeted.\n")
    time.sleep(15)
