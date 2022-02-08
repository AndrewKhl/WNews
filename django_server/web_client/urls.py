from django.urls import path
from . import views

app_name = 'web_client'

urlpatterns = [
    path('', views.home, name='home'),
]
