from django.db import models
from datetime import datetime

from .APIparsers.Models import ArticleModel


class ArticleModelDB(models.Model):
    title = models.CharField(max_length=256, blank=True, null=True)
    text = models.CharField(max_length=256, blank=True, null=True)


class DatabaseStorage:

    @staticmethod
    def save_news(article):
        ArticleModelDB.objects.create(title=article.title, text=article.text)