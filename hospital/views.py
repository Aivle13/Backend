from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from hospital.models import Hospital
import googlemaps
# Create your views here.

@api_view(['POST'])
def signup(request):
    hospital_id = request.data['hospital_id']
    hospital_password = request.data['hospital_password']

    user = User.objects.create_user(username=hospital_id, password=hospital_password)
    token = Token.objects.create(user=user) # 토근 생성
    user.save() # AUTH_USER_MODEL의 User 저장
    
    hospital_name = request.data['hospital_name']
    hospital_address = request.data['hospital_address']
    hospital_phone_number = request.data['hospital_phone_number']
    hospital_department = request.data['hospital_department']
    hospital_longitude = request.data['hospital_longitude']
    hospital_latitude = request.data['hospital_latitude']
    
    hospital = Hospital(author = user,
                      hospital_name = hospital_name,
                      hospital_address = hospital_address, 
                      hospital_phone_number = hospital_phone_number,
                      hospital_department = hospital_department,
                      hospital_longitude = hospital_longitude,
                      hospital_latitude = hospital_latitude,
                      )
    hospital.save()

    return Response(token.key, status=status.HTTP_201_CREATED)