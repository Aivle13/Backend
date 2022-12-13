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

@api_view(['POST'])
def signin(request):
    '''
    로그인
    params: patient_name, patient_password
    return: token 값 (String 형식으로), 200(SUCESS) # 실패에 대한 경우도 생각해야 합니다.
    '''
    hospital_name = request.data['hospital_name']
    hospital_password = request.data['hospital_password']

    user = authenticate(username=hospital_name, password=hospital_password)
    
    if user is None:
        return Response(status=status.HTTP_401_UNAUTHORIZED) # 권한 없음
    try:
        # user를 통해 token get
        token = Token.objects.get(user=user)
    except:
        # [FIX]: token이 없는 경우 (token 생성 이후 기간이 지나 token이 만료되어 사라진 경우) token 재생성
        token = Token.objects.create(user=user)
    return Response(token.key, status=status.HTTP_200_OK)
    