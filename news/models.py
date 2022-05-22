from django.db import models

# Create your models here.


# model site
# title site
# url site url
# type
list_type = (
    ("Article", "Article"),
    ("Media", "Media"),
    ('Bitcoin', 'Bitcoin'),
    ("Trading", "Trading"),
    ("Tweet", "Tweet"),
)


class Site(models.Model):
    title = models.fields.CharField(max_length=50)
    url = models.fields.CharField(max_length=100)
    url_site = models.fields.CharField(max_length=100, null=True)
    type = models.fields.CharField(max_length=20, choices=list_type)

    def __str__(self):
        return f'{self.title} -- {self.url}'


# model Article
    # - title
    # - author
    # - datePubli
    # - decription
    # - category
    # - url
    # - site

class Article(models.Model):
    title = models.fields.CharField(max_length=150)
    author = models.fields.CharField(max_length=40)
    datepubli = models.fields.DateTimeField(auto_now=False)
    description = models.fields.CharField(max_length=2000)
    category_1 = models.fields.CharField(max_length=15, null=True)
    category_2 = models.fields.CharField(max_length=15, null=True)
    category_3 = models.fields.CharField(max_length=15, null=True)
    category_4 = models.fields.CharField(max_length=15, null=True)
    category_environnement = models.fields.BooleanField()
    url = models.fields.URLField(null=True, blank=True)
    site = models.fields.CharField(max_length=20)
    interval_publi = models.fields.CharField(max_length=5, null=True)

    class Meta:
        ordering = ['-datepubli']

    # function for update BD
    def save(self, *args, **kwargs):
        # print('save() is called.')
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} -- {self.site} -- {self.datepubli} -- {self.interval_publi}'


# model Media
    # - title
    # - author
    # - datePubli
    # - decription
    # - url
    # - thumbnail

class Media(models.Model):
    title = models.fields.CharField(max_length=150)
    author = models.fields.CharField(max_length=45)
    datepubli = models.fields.DateTimeField(auto_now=False)
    url = models.fields.URLField(null=True, blank=True)
    category_environnement = models.fields.BooleanField()
    thumbnail = models.ImageField(upload_to='media', blank=True, null=True)
    interval_publi = models.fields.CharField(max_length=5, null=True)

    class Meta:
        ordering = ['-datepubli']

    def __str__(self):
        return f'{self.author} -- {self.title} -- {self.datepubli}'


# model Tweet
    # - title
    # - author
    # - datePubli
    # - url

class Tweet(models.Model):
    title = models.fields.CharField(max_length=300)
    author = models.fields.CharField(max_length=40)
    datepubli = models.fields.DateTimeField(auto_now=False)
    url = models.fields.URLField(null=True, blank=True)
    interval_publi = models.fields.CharField(max_length=5, null=True)

    class Meta:
        ordering = ['-datepubli']

    def __str__(self):
        return f'{self.author} -- {self.title} -- {self.datepubli}'


# model mediaEnvironnement
    # title site

class MediaEnvironnement(models.Model):
    title = models.fields.CharField(max_length=100)

    def __str__(self):
        return f'{self.title}'
