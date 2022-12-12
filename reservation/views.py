from django.shortcuts import render
from rest_framework.decorators import api_view
from reservation.models import Reservation

# Create your views here.
@api_view(['GET'])
def aaa(request):
    # reservations = Reservation.objects.all()
    # print(reservations)
    return