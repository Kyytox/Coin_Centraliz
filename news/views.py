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

    # serveur avec 2 heure de retard en PROD
    # time_change = datetime.timedelta(hours=2)
    # date_now = date_now + time_change

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
    # collect first 100 news media
    for media in Media.objects.all()[:100]:
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
    return render(request, 'news/index.html', {'Latest_articles': Article.objects.all()[:150], 'Latest_media': Media.objects.all()[:100], 'Latest_tweet': Tweet.objects.all()[:100]})


def sites_actus(request):

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
        update_interval_publi = Article.objects.get(title=article.title)
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
        list_append_article = list(Article.objects.filter(
            site=list_site_article[i].title))
        list_all_articles.append(
            [list_site_article[i].title, list_append_article])

    return render(request, 'news/sites_actus.html', {'list_site_article': list_site_article, 'list_all_articles': list_all_articles, 'type_media': type_media, 'count_site': range(count_site)})


def media(request):

    type_media = 'Bitcoin' if request.GET == {} else request.GET['q']

    # collect date now
    date_now = datetime.datetime.now()
    # serveur avec 2 heure de retard en PROD
    # time_change = datetime.timedelta(hours=2)
    # date_now = date_now + time_change

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
        # print('test', media.title)
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
    list_article_environnement = Article.objects.filter(
        category_environnement=True)

    return render(request, 'news/environnement.html', {'list_media_environnement': list_media_environnement, 'list_article_environnement': list_article_environnement})


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

    list_site_actus_article = Site.objects.filter(type='Article')
    list_site_actus_newsletter = Site.objects.filter(type='Newsletter')
    list_site_media_media = Site.objects.filter(type='Media')
    list_site_media_bitcoin = Site.objects.filter(type='Bitcoin')
    list_site_media_trading = Site.objects.filter(type='Trading')

    return render(request, 'news/explication.html', {'list_site_actus_article': list_site_actus_article,
                                                     'list_site_actus_newsletter': list_site_actus_newsletter,
                                                     'list_site_media_media': list_site_media_media,
                                                     'list_site_media_bitcoin': list_site_media_bitcoin,
                                                     'list_site_media_trading': list_site_media_trading, })
