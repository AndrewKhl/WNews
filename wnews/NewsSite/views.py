from django.shortcuts import render


from .MachineLearning.TextManager import TextManager
from .APIparsers.Models import ArticleTagsEnum


def home(request):
    text_manager = TextManager()
    articles, texts = text_manager.get_articles(ArticleTagsEnum.all, 15)

    return render(request, "news_list.html", locals())


def filter_news(request):
    text_manager = TextManager()
    for item in ArticleTagsEnum:
        if item.name in request.GET:
            articles, texts = text_manager.get_articles(item, 15)
    print("IIIIIIIII")
    return render(request, "news_list.html", locals())