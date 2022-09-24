from cgi import test
from datetime import datetime
from doctest import testfile
from pydoc import importfile
from django.shortcuts import render
from numpy import tile
from news.models import Article, Media, Site, Tweet
import datetime
import random
from dateutil.relativedelta import relativedelta
from django.db import connection
from django.db.models import Q
from twitchAPI.twitch import Twitch


def index(request):
    def calcul_interval_date(date_interval):
        if date_interval.days != 0:
            return f'{date_interval.days}j'
        date_decoup = relativedelta(seconds=date_interval.seconds)

        return f'{date_decoup.hours}h' if date_decoup.hours >= 1 else f'{date_decoup.minutes}m'

    date_now = datetime.datetime.now()

    # serveur avec 2 heure de retard en PROD
    # time_change = datetime.timedelta(hours=2)
    # date_now = date_now + time_change

    if request.GET:
        print(request.GET['r'])
        site_type = Site.objects.filter(
            title=request.GET['r']).exclude(type='Newsletter')
        print(site_type[0].type)

        if site_type[0].type == 'Article':
            # Articles
            # collect first 150 news articles
            for article in Article.objects.filter(site=request.GET['r'])[:75]:
                # calcul interval between date no and date publi of article and collect days, hours or minutes.
                date_interval = date_now.replace(
                    tzinfo=datetime.timezone.utc) - article.datepubli

                # calling functions calcul interval date
                interval_publi = calcul_interval_date(date_interval)

                # update BD for add interval_publi
                update_interval_publi_article = Article.objects.get(
                    url=article.url)  # collect line BD with title
                # update champ interval_publi
                update_interval_publi_article.interval_publi = interval_publi
                # make update => call def in Models Article
                update_interval_publi_article.save()

            list_Latest_articles = Article.objects.filter(
                site=request.GET['r'])[:75]
        else:
            list_Latest_articles = Article.objects.all()[:120]
    else:
        #
        # Articles
        # collect first 150 news articles
        for article in Article.objects.all()[:120]:
            # calcul interval between date no and date publi of article and collect days, hours or minutes.
            date_interval = date_now.replace(
                tzinfo=datetime.timezone.utc) - article.datepubli

            # calling functions calcul interval date
            interval_publi = calcul_interval_date(date_interval)

            # update BD for add interval_publi
            update_interval_publi_article = Article.objects.get(
                url=article.url)  # collect line BD with title
            # update champ interval_publi
            update_interval_publi_article.interval_publi = interval_publi
            # make update => call def in Models Article
            update_interval_publi_article.save()

        list_Latest_articles = Article.objects.all()[:120]

    list_site_articles = Site.objects.filter(type='Article')

    return render(request, 'news/main.html', {'Latest_articles': list_Latest_articles,
                                              'list_site_articles': list_site_articles})


def sites_actus(request):

    date_now = datetime.datetime.now()

    type_media = 'Article' if request.GET == {} else request.GET['q']

    date_now = datetime.datetime.now()
    # serveur avec 2 heure de retard en PROD
    # time_change = datetime.timedelta(hours=2)
    # date_now = date_now + time_change

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
        update_interval_publi = Article.objects.get(url=article.url)
        update_interval_publi.interval_publi = interval_publi  # update champ interval_publi
        update_interval_publi.save()  # make update => call def in Models Article

    list_site_article = list(Site.objects.filter(type=type_media))

    # trie random de la liste
    random.shuffle(list_site_article)

    # colect length of list_site_article
    count_site = len(list_site_article)

    list_all_articles = []
    i = 0
    for i in range(count_site):
        list_append_article = list(
            Article.objects.filter(site=list_site_article[i].title))
        list_all_articles.append(
            [list_site_article[i].title, list_append_article])

    return render(request, 'news/sites_actus.html', {'list_site_article': list_site_article, 'list_all_articles': list_all_articles, 'type_media': type_media, 'count_site': range(count_site)})


def media(request):
    def calcul_interval_date(date_interval):
        if date_interval.days != 0:
            return f'{date_interval.days}j'
        date_decoup = relativedelta(seconds=date_interval.seconds)

        return f'{date_decoup.hours}h' if date_decoup.hours >= 1 else f'{date_decoup.minutes}m'

    date_now = datetime.datetime.now()

    # serveur avec 2 heure de retard en PROD
    # time_change = datetime.timedelta(hours=2)
    # date_now = date_now + time_change

    if request.GET:
        print(request.GET['r'])
        site_type = Site.objects.filter(
            title=request.GET['r']).exclude(type='Newsletter')
        print(site_type[0].type)

        if site_type[0].type == 'Article':
            list_Latest_media = Media.objects.all()[:75]
        else:
            # Media
            # collect first 100 news media
            for media in Media.objects.filter(author=request.GET['r'])[:50]:
                # calcul interval between date no and date publi of article and collect days, hours or minutes
                date_interval = date_now.replace(
                    tzinfo=datetime.timezone.utc) - media.datepubli

                # calling functions calcul interval date
                interval_publi = calcul_interval_date(date_interval)

                # update BD for add interval_publi
                # collect line BD with title
                # print("titre :", media.title)
                update_interval_publi_media = Media.objects.get(url=media.url)
                # update champ interval_publi
                update_interval_publi_media.interval_publi = interval_publi
                update_interval_publi_media.save()  # make update => call def in Models Media
            # list_Latest_articles = Article.objects.all()[:120]
            list_Latest_media = Media.objects.filter(
                author=request.GET['r'])[:50]
            # list_Latest_tweet = Tweet.objects.all()[:50]
    else:
        #
        # Media
        # collect first 100 news media
        for media in Media.objects.all()[:100]:
            # calcul interval between date no and date publi of article and collect days, hours or minutes
            date_interval = date_now.replace(
                tzinfo=datetime.timezone.utc) - media.datepubli

            # calling functions calcul interval date
            interval_publi = calcul_interval_date(date_interval)

            # update BD for add interval_publi
            # collect line BD with title
            # print("titre :", media.title)
            update_interval_publi_media = Media.objects.get(url=media.url)
            # update champ interval_publi
            update_interval_publi_media.interval_publi = interval_publi
            update_interval_publi_media.save()  # make update => call def in Models Media

        list_Latest_media = Media.objects.all()[:100]

    list_site_media_media = Site.objects.filter(type='Media')
    list_site_media_bitcoin = Site.objects.filter(type='Bitcoin')
    list_site_media_trading = Site.objects.filter(type='Trading')

    return render(request, 'news/youtube.html', {'Latest_media': list_Latest_media,
                                                 'list_site_media_media': list_site_media_media,
                                                 'list_site_media_bitcoin': list_site_media_bitcoin,
                                                 'list_site_media_trading': list_site_media_trading, })


def live(request):
    #
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
        viewer_count = stream['viewer_count']
        thumbnail_url_stream = stream['thumbnail_url']
        thumbnail_url_stream = thumbnail_url_stream.replace("{width}", "300")
        thumbnail_url_stream = thumbnail_url_stream.replace("{height}", "170")

        if 'ㅿㅁㅇ' in user_name:
            continue
        req_user = twitch.get_users(logins=[user_name])
        list_infos_user = req_user['data']
        for user in list_infos_user:
            thumbnail_url_user = user['profile_image_url']

            list_stream_online.append(
                [user_name, title, viewer_count, thumbnail_url_stream, thumbnail_url_user])

    return render(request, 'news/twitch.html', {'list_stream_online': list_stream_online})


def newsletter(request):

    list_newsletter = list(Site.objects.filter(type="Newsletter"))

    print(list_newsletter)

    return render(request, 'news/newsletters.html', {'list_newsletters': list_newsletter})


def tweets(request):
    def calcul_interval_date(date_interval):
        if date_interval.days != 0:
            return f'{date_interval.days}j'
        date_decoup = relativedelta(seconds=date_interval.seconds)

        return f'{date_decoup.hours}h' if date_decoup.hours >= 1 else f'{date_decoup.minutes}m'

    date_now = datetime.datetime.now()

    # Tweet
    # collect first 100 news Tweet
    for tweet in Tweet.objects.all()[:50]:
        # calcul interval between date no and date publi of article and collect days, hours or minutes
        date_interval = date_now.replace(
            tzinfo=datetime.timezone.utc) - tweet.datepubli

        # calling functions calcul interval date
        interval_publi = calcul_interval_date(date_interval)

        # update BD for add interval_publi
        # collect line BD with title
        update_interval_publi_tweet = Tweet.objects.get(url=tweet.url)
        # update champ interval_publi
        update_interval_publi_tweet.interval_publi = interval_publi
        update_interval_publi_tweet.save()  # make update => call def in Models tweet

    list_tweets = Tweet.objects.all()[:100]
    print(list_tweets)

    return render(request, 'news/tweets.html', {'list_tweets': list_tweets})


def environnement(request):

    list_media_environnement = Media.objects.filter(
        category_environnement=True)
    list_article_environnement = Article.objects.filter(
        category_environnement=True)

    return render(request, 'news/environnement.html', {'Latest_media': list_media_environnement, 'list_article_environnement': list_article_environnement})


def SearchPage(request):

    search_term = ''
    category = ''
    list_articles = []
    list_youtube = []
    list_tweet = []

    search_term = request.GET['q']

    if len(request.GET) == 2:
        category = request.GET['c']

    if category == '':
        if Article.objects.filter(title__icontains=search_term):
            list_articles = Article.objects.filter(
                title__icontains=search_term)
            list_youtube = Media.objects.filter(
                title__icontains=search_term)[:1]
            list_tweet = Tweet.objects.filter(title__icontains=search_term)[:1]

        elif Media.objects.filter(title__icontains=search_term):
            list_youtube = Media.objects.filter(title__icontains=search_term)
            list_articles = Article.objects.filter(
                title__icontains=search_term)[:1]
            list_tweet = Tweet.objects.filter(title__icontains=search_term)[:1]

        elif Tweet.objects.filter(title__icontains=search_term):
            list_tweet = Tweet.objects.filter(title__icontains=search_term)
            list_articles = Article.objects.filter(
                title__icontains=search_term)[:1]
            list_youtube = Media.objects.filter(
                title__icontains=search_term)[:1]

    elif category == 'article':
        list_articles = Article.objects.filter(title__icontains=search_term)
        list_youtube = Media.objects.filter(title__icontains=search_term)[:1]
        list_tweet = Tweet.objects.filter(title__icontains=search_term)[:1]

    elif category == 'youtube':
        list_youtube = Media.objects.filter(title__icontains=search_term)
        list_articles = Article.objects.filter(
            title__icontains=search_term)[:1]
        list_tweet = Tweet.objects.filter(title__icontains=search_term)[:1]

    elif category == 'tweets':
        list_tweet = Tweet.objects.filter(title__icontains=search_term)
        list_articles = Article.objects.filter(
            title__icontains=search_term)[:1]
        list_youtube = Media.objects.filter(title__icontains=search_term)[:1]

    return render(request, 'news/searchPage.html', {'Latest_articles': list_articles, 'Latest_media': list_youtube, 'list_tweets': list_tweet, 'search_term': search_term})


def SearchCategory(request):

    catogery_term = request.GET['q']
    list_articles = Article.objects.filter(Q(category_1=catogery_term) | Q(
        category_2=catogery_term) | Q(category_3=catogery_term) | Q(category_4=catogery_term))

    return render(request, 'news/searchCategory.html', {'Latest_articles': list_articles})


def explication(request):

    list_site_actus_article = Site.objects.filter(type='Article')
    list_site_actus_newsletter = Site.objects.filter(type='Newsletter')
    list_site_media_media = Site.objects.filter(type='Media')
    list_site_media_bitcoin = Site.objects.filter(type='Bitcoin')
    list_site_media_trading = Site.objects.filter(type='Trading')
    list_site_media_twitch = Site.objects.filter(type='Twitch')

    return render(request, 'news/explication.html', {'list_site_actus_article': list_site_actus_article,
                                                     'list_site_actus_newsletter': list_site_actus_newsletter,
                                                     'list_site_media_media': list_site_media_media,
                                                     'list_site_media_bitcoin': list_site_media_bitcoin,
                                                     'list_site_media_trading': list_site_media_trading,
                                                     'list_site_media_twitch': list_site_media_twitch})
