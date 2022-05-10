from django.contrib import admin
from news.models import Site, Article, Media, MediaEnvironnement, Tweet


# Register your models here.
admin.site.register(Article)
admin.site.register(Site)
admin.site.register(Media)
admin.site.register(MediaEnvironnement)
admin.site.register(Tweet)
