from django.urls import path

from reservation.views import reservation, hospital_get_delete_reservation

urlpatterns = [
    path('', hospital_get_delete_reservation),
    path('reservation/', reservation),
]
