from django.urls import path

from reservation.views import reservation, reservation_cancel, hospital_get_delete_reservation

urlpatterns = [
    path('', hospital_get_delete_reservation),
    path('reservation/', reservation),
    path('cancel/', reservation_cancel),
]
