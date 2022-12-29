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
        hospital_name =  request.data['name'] # 병원 이름
        hospital_address = request.data['address'] # 병원 주소
        reservation_comment =  request.data['reservation_comment'] # 문진표
        patient = Patient.objects.get(author=user.id) #환자 객체
        hospital = Hospital.objects.get(hospital_name = hospital_name, hospital_address = hospital_address)

        reservation_hospital_data = Reservation.objects.filter(hospital=hospital) #예약되있는 병원들만 빼옴
        reservation_patient_data = Reservation.objects.filter(patient=patient)
        
        if(reservation_patient_data.count() >= 1): #이미 예약이 되어있는지 확인
            if reservation_patient_data[0].reservation_state == 'C':
                pass
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        
        patient_count = 0
        
        for i in range(reservation_hospital_data.count()): # 환자 객체끼리 비교
            if patient == reservation_hospital_data[i].patient and reservation_hospital_data[i].reservation_state != 'C': 
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

        return Response(status=status.HTTP_200_OK)
    
    elif request.method == 'GET':
        hospital_name = request.GET['name']
        hospital_address = request.GET['address']
        patient = Patient.objects.get(author=user.id) #환자 객체
        # 병원 선택
        hospital = Hospital.objects.get(hospital_name = hospital_name, hospital_address = hospital_address)
        # 해당 병원 예약 승인 대기중
        patient_request = Reservation.objects.filter(hospital = hospital, patient = patient, reservation_state = "A")

        if patient_request.count() < 1: # 예약이 안되어있다면 404에러
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        myturn = 0
        
        patient_data = Reservation.objects.filter(hospital = hospital, reservation_state = "A") #환자 명수
        patient_pk = Reservation.objects.get(patient = patient, reservation_state = "A") # 고객 번호
        
        if patient_data.count() < 1: #환자가 없으면
            return Response(status=status.HTTP_404_NOT_FOUND)
    
        for i in range(patient_data.count()):
            if patient == patient_data[i].patient:
                myturn = i+1

        data = {
            'wait_count': patient_data.count(),
            'user_count' : patient_pk.pk,
            'my_turn' : myturn
        }
        
        return Response(data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def reservation_cancel(request):
    user = request.user
    patient = Patient.objects.get(author=user.id)
    hospital_name = request.GET['name']
    hospital_address = request.GET['address']
    hospital = Hospital.objects.get(hospital_name = hospital_name, hospital_address = hospital_address)
    try :
        patient_data = Reservation.objects.get(patient = patient, hospital = hospital, reservation_state = "P") # 고객 번호
    except:
        patient_data = Reservation.objects.get(patient = patient, hospital = hospital, reservation_state = "A") # 고객 번호
    print(patient_data)
    patient_data.delete()
    return Response(status=status.HTTP_200_OK)


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
    
    
