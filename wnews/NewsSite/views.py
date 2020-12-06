import sched, time

from threading import Thread
from django.shortcuts import render

from .MachineLearning.TextManager import TextManager
from .APIparsers.Models import ArticleTagsEnum
from .models import DatabaseStorage

update_thread = None

text_manager = TextManager()
news_storage = DatabaseStorage()
news_scheduler = sched.scheduler(time.time, time.sleep)


def home(request):
    #articles, texts = text_manager.get_articles(ArticleTagsEnum.sport, 15)

    #for article in articles:
    #    article.tag = ArticleTagsEnum.sport
    #    news_storage.save_news(article)
    update_thread = Thread(target=run_news_updates)
    articles = news_storage.get_articles(ArticleTagsEnum.sport)
    update_thread.start()

    return render(request, "news_list.html", locals())


def filter_news(request):
    for item in ArticleTagsEnum:
        if item.name in request.GET:
            articles, texts = text_manager.get_articles(item, 15)
    return render(request, "news_list.html", locals())


def run_news_updates():
    update_news()
    news_scheduler.run()


def update_news():
    articles = text_manager.get_new_articles(ArticleTagsEnum.sport)

    if len(articles) > 0:
        for article in articles:
            article.tag = ArticleTagsEnum.sport
            news_storage.save_news(article)
    else:
        print("New news not be found")

    news_scheduler.enter(10, 1, update_news)

