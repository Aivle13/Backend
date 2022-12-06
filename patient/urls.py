from django.urls import path
from patient.views import signup, signin

urlpatterns = [
    path('signup/', signup),
    path('signin/', signin),
]
