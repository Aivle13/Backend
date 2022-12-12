from django.urls import path
from hospital.views import signup

urlpatterns = [
    path('signup/', signup),
]