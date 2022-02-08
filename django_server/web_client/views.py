from django.shortcuts import render


def home(request):
    return render(request, "news_list.html", locals())