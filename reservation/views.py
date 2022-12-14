from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

from patient.models import Patient
from hospital.models import Hospital
from reservation.models import Reservation
# Create your views here.

@api_view(['POST'])
def reservation(request):
    hospital_name =  request.data['hospital_state'] # 병원 이름
    reservation_comment =  request.data['reservation_comment'] # 문진표
    user = request.user # token을 통해 Auth user를 가져옴
    patient = Patient.objects.get(author=user.id) #환자 객체
    hospital = Hospital.objects.get(hospital_name = hospital_name)
    #hospital = Hospital.objects.get(hospital_name = 'Bệnh viện Bình Dân')
    # 오류날 시 hospital_name -> 본인이 등록한 병원 입력해 넣으세요
    
    reservation = Reservation(
                    reservation_comment = str(reservation_comment),
                    patient = patient,
                    hospital = hospital,
                    )
    reservation.save()
    
    hospital_data = Reservation.objects.filter(hospital=hospital)
    print()
    print("남은 인원 수 : " + str(hospital_data.count()))
    print(str(reservation.pk)+ "번 고객님" ) #현재 등록한 프라이머리 키
    
    data = {
        'wait_count': hospital_data.count(),
        'user_count' : reservation.pk
    }
    
    return Response(data, status=status.HTTP_200_OK)