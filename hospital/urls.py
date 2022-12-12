from django.urls import path
from hospital.views import signup
from hospital.views import signin

urlpatterns = [
    path('signup/', signup),
    path('signin/', signin),
]