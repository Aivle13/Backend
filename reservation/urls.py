from django.urls import path
from reservation.views import reservation

urlpatterns = [
    path('reservation/', reservation),
]
