
from django.contrib import admin
from django.urls import path
from news.views import index, sites_actus, media, live, newsletter, tweets, environnement, SearchPage, SearchCategory, explication

urlpatterns = [
    path('', index, name='index'),
    path('sites_actus/', sites_actus, name='sites_actus'),
    path('media/', media, name='media'),
    path('live/', live, name='live'),
    path('newsletter/', newsletter, name='newsletter'),
    path('tweets/', tweets, name='tweets'),
    path('environnement/', environnement, name='environnement'),
    path('searchPage/', SearchPage, name='SearchPage'),
    path('searchCategory/', SearchCategory, name='searchCategory'),
    path('explication/', explication, name='explication'),
    path('admin/', admin.site.urls),
]
