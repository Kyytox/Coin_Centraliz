from cgi import test
from datetime import datetime
from doctest import testfile
from pydoc import importfile
from django.shortcuts import render
from news.models import Article, Media, Site, Tweet
import datetime
import random
from dateutil.relativedelta import relativedelta
from django.db import connection
from django.db.models import Q


def index(request):

    def calcul_interval_date(date_interval):
        if date_interval.days != 0:
            return f'{date_interval.days}j'
        date_decoup = relativedelta(seconds=date_interval.seconds)

        return f'{date_decoup.hours}h' if date_decoup.hours >= 1 else f'{date_decoup.minutes}m'

    date_now = datetime.datetime.now()

    #
    # Articles
    # collect first 150 news articles
    for article in Article.objects.all()[:150]:
        # calcul interval between date no and date publi of article and collect days, hours or minutes.
        date_interval = date_now.replace(
            tzinfo=datetime.timezone.utc) - article.datepubli

        # calling functions calcul interval date
        interval_publi = calcul_interval_date(date_interval)

        # update BD for add interval_publi
        update_interval_publi_article = Article.objects.get(
            title=article.title)  # collect line BD with title
        # update champ interval_publi
        update_interval_publi_article.interval_publi = interval_publi
        # make update => call def in Models Article
        update_interval_publi_article.save()

    #
    # Media
    # collect first 50 news media
    for media in Media.objects.all()[:50]:
        # calcul interval between date no and date publi of article and collect days, hours or minutes
        date_interval = date_now.replace(
            tzinfo=datetime.timezone.utc) - media.datepubli

        # calling functions calcul interval date
        interval_publi = calcul_interval_date(date_interval)

        # update BD for add interval_publi
        # collect line BD with title
        update_interval_publi_media = Media.objects.get(title=media.title)
        # update champ interval_publi
        update_interval_publi_media.interval_publi = interval_publi
        update_interval_publi_media.save()  # make update => call def in Models Media

    #
    # Tweet
    # collect first 100 news Tweet
    for tweet in Tweet.objects.all()[:100]:
        # calcul interval between date no and date publi of article and collect days, hours or minutes
        date_interval = date_now.replace(
            tzinfo=datetime.timezone.utc) - tweet.datepubli

        # calling functions calcul interval date
        interval_publi = calcul_interval_date(date_interval)

        # update BD for add interval_publi
        # collect line BD with title
        update_interval_publi_tweet = Tweet.objects.get(title=tweet.title)
        # update champ interval_publi
        update_interval_publi_tweet.interval_publi = interval_publi
        update_interval_publi_tweet.save()  # make update => call def in Models tweet

    # we retrieve the first x Article-Media-Tweet with new interval date publi
    return render(request, 'news/index.html', {'Latest_articles': Article.objects.all()[:150], 'Latest_media': Media.objects.all()[:50], 'Latest_tweet': Tweet.objects.all()[:100]})


def sites_actus(request):

    date_now = datetime.datetime.now()

    # collect all media for add interval publication
    list_article = Article.objects.all()

    for article in list_article:
        # calcul interval between date no and date publi of article and collect days, hours or minutes.
        new_time = article.datepubli

        date_interval = date_now.replace(
            tzinfo=datetime.timezone.utc) - new_time

        if date_interval.days != 0:
            interval_publi = (f'{date_interval.days}j')
        else:
            date_decoup = relativedelta(seconds=date_interval.seconds)

            if date_decoup.hours >= 1:
                interval_publi = (f'{date_decoup.hours}h')
            else:
                interval_publi = (f'{date_decoup.minutes}m')

        # update BD for add interval_publi
        # collect line BD with title
        update_interval_publi = Article.objects.get(title=article.title)
        update_interval_publi.interval_publi = interval_publi  # update champ interval_publi
        update_interval_publi.save()  # make update => call def in Models Article

    list_site_article = list(Site.objects.filter(type='Article'))

    # trie random de la liste
    random.shuffle(list_site_article)

    # colect length of list_site_article
    count_site = len(list_site_article)

    list_all_articles = []
    i = 0
    for i in range(count_site):
        list_append_article = list(Article.objects.filter(
            site=list_site_article[i].title))
        list_all_articles.append(
            [list_site_article[i].title, list_append_article])

    return render(request, 'news/sites_actus.html', {'list_site_article': list_site_article, 'list_all_articles': list_all_articles, 'count_site': range(count_site)})


def media(request):

    type_media = 'Media' if request.GET == {} else request.GET['q']

    # collect date now
    date_now = datetime.datetime.now()

    # collect all media for add interval publication
    list_media = Media.objects.all()

    # collect url of 1 media with random index
    random_index = random.randint(0, len(list_media))

    random_media = []
    random_media = list_media[random_index]

    for media in list_media:
        # calcul interval between date no and date publi of article and collect days, hours or minutes
        date_interval = date_now.replace(
            tzinfo=datetime.timezone.utc) - media.datepubli

        if date_interval.days != 0:
            interval_publi = (f'{date_interval.days}j')
        else:
            date_decoup = relativedelta(seconds=date_interval.seconds)

            if date_decoup.hours >= 1:
                interval_publi = (f'{date_decoup.hours}h')
            else:
                interval_publi = (f'{date_decoup.minutes}m')

        # update BD for add interval_publi
        # collect line BD with title
        update_interval_publi_media = Media.objects.get(title=media.title)
        # update champ interval_publi
        update_interval_publi_media.interval_publi = interval_publi
        update_interval_publi_media.save()  # make update => call def in Models Media

    list_site_media = list(Site.objects.filter(type=type_media))

    # trie random de la liste
    random.shuffle(list_site_media)

    # colect length of list_site_article
    count_site = len(list_site_media)

    list_all_media = []
    i = 0
    for i in range(count_site):
        list_append_media = list(Media.objects.filter(
            author=list_site_media[i].title))
        list_all_media.append([list_site_media[i].title, list_append_media])

    return render(request, 'news/media.html', {'list_site_media': list_site_media, 'list_all_media': list_all_media, 'type_media': type_media, 'count_site': range(count_site), 'random_media': random_media})


def environnement(request):

    list_media_environnement = Media.objects.filter(
        category_environnement=True)

    return render(request, 'news/environnement.html', {'list_media_environnement': list_media_environnement})


def SearchPage(request):

    search_term = ''
    search_term = request.GET['q']
    list_articles = Article.objects.filter(title__icontains=search_term)
    list_media = Media.objects.filter(title__icontains=search_term)
    list_tweet = Tweet.objects.filter(title__icontains=search_term)

    return render(request, 'news/searchPage.html', {'list_articles': list_articles, 'list_media': list_media, 'list_tweet': list_tweet})


def SearchCategory(request):

    catogery_term = request.GET['q']
    list_articles = Article.objects.filter(Q(category_1=catogery_term) | Q(
        category_2=catogery_term) | Q(category_3=catogery_term) | Q(category_4=catogery_term))

    return render(request, 'news/searchCategory.html', {'list_articles': list_articles})


def explication(request):

    list_site_article = Site.objects.filter(type='Article')
    list_site_media = Site.objects.filter(type='Media')

    return render(request, 'news/explication.html', {'list_site_article': list_site_article, 'list_site_media': list_site_media})

# list_site_ajout = [
# ['CryptoNews', 'https://fr.cryptonews.com/news/feed/', 'https://fr.cryptonews.com/', 'Article'],
#                    ['Journal du coin', 'https://journalducoin.com/', 'https://journalducoin.com/feed/', 'Article'],
#                    ['CryptToast', 'https://cryptoast.fr/', 'https://cryptoast.fr/feed/', 'Article'],
#                    ['CoinAcademy', 'https://coinacademy.fr/', 'https://coinacademy.fr/feed/', 'Article'],
#                    ['Bitcoin.fr', 'https://bitcoin.fr/', 'https://bitcoin.fr/feed/', 'Article'],
#                    ['Coins.fr', 'https://coins.fr/', 'https://coins.fr/feed/', 'Article'],
#                    ['Cointribune', 'https://www.cointribune.com/', 'https://www.cointribune.com/feed/', 'Article'],
#                    ['CryptoActu', 'https://cryptoactu.com/', 'https://cryptoactu.com/feed/', 'Article'],
#                    ['Grand Angle Crypto', 'https://www.youtube.com/channel/UCT5FYQ_io06t7aY8rShgzvA',
#                     'https://www.youtube.com/feeds/videos.xml?channel_id=UCT5FYQ_io06t7aY8rShgzvA', 'Media'],
#                    ['Découvre Bitcoin', 'https://www.youtube.com/channel/UCANjJ55UmYmoXm_SW--psXQ', 'https://www.youtube.com/feeds/videos.xml?channel_id=UCANjJ55UmYmoXm_SW--psXQ', 'Media'],
#                    ['Surfin' Bitcoin', 'https://www.youtube.com/channel/UChfepkLjWJzSW16QArGYxWg', 'https://www.youtube.com/feeds/videos.xml?channel_id=UChfepkLjWJzSW16QArGYxWg', 'Media'],
#                    ['Univers Bitcoin Podcast', 'https://www.youtube.com/channel/UCOlhr_6OnEnqV8wrbrnLZvQ', 'https://www.youtube.com/feeds/videos.xml?channel_id=UCOlhr_6OnEnqV8wrbrnLZvQ', 'Media'],
#                    ['Parlons Bitcoin', 'https://www.youtube.com/channel/UCBLCX3V2DeoP1wrEfxG-z0g', 'https://www.youtube.com/feeds/videos.xml?channel_id=UCBLCX3V2DeoP1wrEfxG-z0g', 'Media'],
#                    ['Parlons Crypto - L'émission', 'https://www.youtube.com/channel/UCx3KJIw43_1q4gKpJkiaRJg', 'https://www.youtube.com/feeds/videos.xml?channel_id=UCx3KJIw43_1q4gKpJkiaRJg', 'Media'],
#                    ['Journal du Coin', 'https://www.youtube.com/channel/UC7qnB0XxzOEwWWn9Q6HPmCw', 'https://www.youtube.com/feeds/videos.xml?channel_id=UC7qnB0XxzOEwWWn9Q6HPmCw', 'Media'],
#                    ['Cryptoast', 'https://www.youtube.com/channel/UCD9yJ3yOv6hCMeYLYAVi7zw', 'https://www.youtube.com/feeds/videos.xml?channel_id=UCD9yJ3yOv6hCMeYLYAVi7zw', 'Media'],
#                    ['Hasheur', 'https://www.youtube.com/channel/UChlTcWDE8gd4tsl_L727NrQ', 'https://www.youtube.com/feeds/videos.xml?channel_id=UChlTcWDE8gd4tsl_L727NrQ', 'Media'],
#                    ['Crypto Farmeur', 'https://www.youtube.com/channel/UCJQ5j2qqWWOj800lCrsb34g', 'https://www.youtube.com/feeds/videos.xml?channel_id=UCJQ5j2qqWWOj800lCrsb34g', 'Media'],
#                    ['Crok - Crypto News', 'https://www.youtube.com/channel/UCOJzqoA84sSqdfkF5hw3Uyg', 'https://www.youtube.com/feeds/videos.xml?channel_id=UCOJzqoA84sSqdfkF5hw3Uyg', 'Media'],
#                    ['Monsieur-TK', 'https://www.youtube.com/channel/UC0DITweI6K01RpfrJDMQWFw', 'https://www.youtube.com/feeds/videos.xml?channel_id=UC0DITweI6K01RpfrJDMQWFw', 'Media'],
#                    ['CryptoLogik', 'https://www.youtube.com/channel/UCU5xRfYU2CZHyoFwmHVFipw', 'https://www.youtube.com/feeds/videos.xml?channel_id=UCU5xRfYU2CZHyoFwmHVFipw', 'Media'],
#                    ['fund3r community', 'https://www.youtube.com/channel/UCJwSVnTxXFOoR8E_iBPHbpw', 'https://www.youtube.com/feeds/videos.xml?channel_id=UCJwSVnTxXFOoR8E_iBPHbpw', 'Media'],
#                    ['DeFi France', 'https://www.youtube.com/channel/UCztkHfSVCdriSpzvZF7Qwtg', 'https://www.youtube.com/feeds/videos.xml?channel_id=UCztkHfSVCdriSpzvZF7Qwtg', 'Media'],
#                    ['Decryptalk', 'https://www.youtube.com/channel/UCi7NBlzOjoSgRcE7GQpRp6Q', 'https://www.youtube.com/feeds/videos.xml?channel_id=UCi7NBlzOjoSgRcE7GQpRp6Q', 'Media'],
#                    ['Learn & Earn Crypto Podcast [Francophone]', 'https://www.youtube.com/channel/UCbnFckir-MItQ1uAWtZ4RNA', 'https://www.youtube.com/feeds/videos.xml?channel_id=UCbnFckir-MItQ1uAWtZ4RNA', 'Media'],
#                    ['21 Millions', 'https://www.youtube.com/channel/UCVQ4B7feh8kCMwxL4ncX7UA', 'https://www.youtube.com/feeds/videos.xml?channel_id=UCVQ4B7feh8kCMwxL4ncX7UA', 'Media'],
#     ['Wave Trading France', 'https://www.youtube.com/channel/UCQN2wjWxpMdDeaz7_El1nxg',
#         'https://www.youtube.com/feeds/videos.xml?channel_id=UCQN2wjWxpMdDeaz7_El1nxg', 'Trading'],
#     ['Enter The Crypto Matrix', 'https://www.youtube.com/channel/UCefQC4Y-X9MBRuYBKc2waiQ', 'https://www.youtube.com/feeds/videos.xml?channel_id=UCefQC4Y-X9MBRuYBKc2waiQ', 'Media'],
#     ['Crypto Picsou', 'https://www.youtube.com/channel/UCZioDtSSkxEmeN0Iqv9neHA', 'https://www.youtube.com/feeds/videos.xml?channel_id=UCZioDtSSkxEmeN0Iqv9neHA', 'Media'],
#     ['Khalistas to the moon', 'https://www.youtube.com/channel/UCUE_Y-qamqLT-5bsihtCphw', 'https://www.youtube.com/feeds/videos.xml?channel_id=UCUE_Y-qamqLT-5bsihtCphw', 'Trading'],
#     ['Captain Trading', 'https://www.youtube.com/channel/UCJdx6xfJVFLXJuv9I7ECuRA', 'https://www.youtube.com/feeds/videos.xml?channel_id=UCJdx6xfJVFLXJuv9I7ECuRA', 'Trading']]


# for x in list_site_ajout:
#     print('x: ', x[0])
#     bd_insert = Site.objects.create(
#         title=x[0],
#         url=x[2],
#         url_site=x[1]
#         type=x[3])
