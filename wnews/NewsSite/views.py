from django.shortcuts import render


from .MachineLearning.TextManager import TextManager
from .APIparsers.Models import ArticleTagsEnum


def home(request):
    text_manager = TextManager()
    articles, texts = text_manager.get_articles(ArticleTagsEnum.all, 15)

    return render(request, "news_list.html", locals())
