from django.contrib import admin
from django.urls import path, include
from user.views import signup, signin

urlpatterns = [
    path('signup/', signup),
    path('signin/', signin),
]
