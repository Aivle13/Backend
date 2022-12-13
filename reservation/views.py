from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from django.contrib.auth import get_user

from patient.models import Patient
from hospital.models import Hospital
from reservation.models import Reservation
# Create your views here.

""" @api_view(['POST'])
def reservation(request):
    # Create your views here. """
@api_view(['GET'])
def reservation(request):
    hospital_name =  request.GET.get('hospital_state') # 병원 이름
    reservation_comment =  request.GET.get('reservation_comment') # 문진표
    user = request.user # token을 통해 Auth user를 가져옴
    patient = Patient.objects.get(author=user.id) #환자 객체
    hospital = Hospital.objects.get(hospital_name = hospital_name)
    # 오류날 시 hospital_name -> 본인이 등록한 병원 입력해 넣으세요
    
    reservation = Reservation(
                    reservation_comment = str(reservation_comment),
                    patient = patient,
                    hospital = hospital,
                    )
    reservation.save()

    return Response(status=status.HTTP_200_OK)