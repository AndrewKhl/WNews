from django.shortcuts import render


def home(request):
    tenant = request.tenant
    print('Toooooooo')
    print(tenant)
    return render(request, "news_list.html", locals())