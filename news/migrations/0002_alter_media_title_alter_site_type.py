# Generated by Django 4.0.1 on 2022-05-25 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='title',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='site',
            name='type',
            field=models.CharField(choices=[('Article', 'Article'), ('Newsletter', 'Newsletter'), ('Media', 'Media'), ('Bitcoin', 'Bitcoin'), ('Trading', 'Trading'), ('Twitch', 'Twitch'), ('Tweet', 'Tweet')], max_length=20),
        ),
    ]
