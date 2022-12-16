from django.urls import path
from hospital.views import signup
from hospital.views import signin
from hospital.views import mypage

urlpatterns = [
    path('signup/', signup),
    path('signin/', signin),
    path('mypage/', mypage),
]