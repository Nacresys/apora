
from django.contrib import admin
from django.urls import path, include

from login import views

app_name='main_login'

urlpatterns = [
    path('',views.login,name = 'login'),
]