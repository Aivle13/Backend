from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

from patient.models import Patient
from hospital.models import Hospital
from reservation.models import Reservation

from django.core import serializers
from django.db.models import Q

# Create your views here.

@api_view(['POST','GET'])
def reservation(request):
    user = request.user # token을 통해 Auth user를 가져옴
    if request.method == 'POST':
        hospital_name =  request.data['hospital_state'] # 병원 이름
        reservation_comment =  request.data['reservation_comment'] # 문진표
        patient = Patient.objects.get(author=user.id) #환자 객체
        hospital = Hospital.objects.get(hospital_name = hospital_name) #병원객체
        reservation_data = Reservation.objects.filter(hospital=hospital) #예약되있는 병원들만 빼옴
        
        patient_count = 0
        
        for i in range(reservation_data.count()):
            if patient == reservation_data[i].patient: #환자 객체끼리 비교
                patient_count += 1
                print(patient_count)
                
        if patient_count > 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            pass


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
            'user_count' : reservation.pk,
            'my_turn' : hospital_data.count()
        }
        

        return Response(data, status=status.HTTP_200_OK)
    
    elif request.method == 'GET':
        hospital_name = request.GET['state']
        print(user.id)
        patient = Patient.objects.get(author=user.id) #환자 객체
        print(patient)
        hospital = Hospital.objects.get(hospital_name = hospital_name)
        patient_data = Reservation.objects.filter(hospital=hospital)
        patient_pk = Reservation.objects.get(patient = patient)
        
        print(patient_data[0].patient)
        
        myturn = 0
        
        for i in range(patient_data.count()):
            if patient == patient_data[i].patient:
                myturn = i+1

        data = {
            'wait_count': patient_data.count(),
            'user_count' : patient_pk.pk,
            'my_turn' : myturn
        }
        
        return Response(data, status=status.HTTP_200_OK)
    
    
@api_view(['GET', 'POST'])
def hospital_get_delete_reservation(request):
    
    user = request.user
    # 진단표 가져오기 (in HOSPITAL)
    try:
        state = request.data['reservation_state']
        print(request.data['reservation_state'])

        hospital = Hospital.objects.get(author=user.id)
        reservations = serializers.serialize('json', Reservation.objects.filter(Q(hospital=hospital) & Q(reservation_state = state)))

        return Response(reservations, status=status.HTTP_200_OK)
        
    # 승인 (in HOSPITAL)
    except: 
        reservation_id = request.data['reservation_id']
        change_state = request.data['change_state']
        print(request.data['reservation_id'])

        reservation = Reservation.objects.get(id=reservation_id)
        reservation.reservation_state = change_state 
        reservation.save()

        return Response(status=status.HTTP_200_OK)
