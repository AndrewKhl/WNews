from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    news_titles = ["{} title".format(i) for i in range(14)]
    texts = ["Default text {}".format(i) for i in range(14)]

    articles = [Article(title, text) for title, text in zip(news_titles, texts)]

    return render(request, "news_list.html", locals())


class Article:
    title = ""
    text = ""

    def __init__(self, title, text):
        self.title = title
        self.text = text
