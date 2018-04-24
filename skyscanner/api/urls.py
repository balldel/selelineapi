from django.urls import path,include
from django.contrib import admin
from .views import Bot, Country

app_name = 'selelineapi'

urlpatterns = [
    path('country/', Country.as_view(), name="country"),
    path('bot/', Bot.as_view(), name="bot"),
    
]