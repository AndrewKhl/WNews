from django.shortcuts import render

from .MachineLearning.TextManager import TextManager
from .APIparsers.Models import ArticleTagsEnum


text_manager = TextManager()


def home(request):
    articles, texts = text_manager.get_articles(ArticleTagsEnum.all, 15)
    return render(request, "news_list.html", locals())


def filter_news(request):
    for item in ArticleTagsEnum:
        if item.name in request.GET:
            articles, texts = text_manager.get_articles(item, 15)
    return render(request, "news_list.html", locals())