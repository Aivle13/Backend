from django.shortcuts import get_object_or_404

# DRF (Django Rest Framework)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Token을 통해 현재 요청하는 사람이 누군지를 판단: 
#   Token은 로그인한 사용자가 요청시 Header에 함께 보냄
#   고로 login은 Token을 받는 과정
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

# Model (CRUD 대상)
from patient.models import Patient



@api_view(['POST'])
def signup(request):
    '''
    회원가입
    params: patient_name, patient_password, patient_birth, patient_email
    return: 201(SUCESS) # 실패에 대한 경우도 생각해야 합니다.
    '''
    patient_name = request.data['patient_name']
    patient_password = request.data['patient_password']

    user = User.objects.create_user(username=patient_name, password=patient_password)
    token = Token.objects.create(user=user) # 토근 생성
    user.save() # AUTH_USER_MODEL의 User 저장

    try:
        patient_birth = request.data['patient_birth']
        patient_email = request.data['patient_email']
    except:
        patient_birth = '1998-05-21'
        patient_email = ''

    patient = Patient(author=user, patient_birth=patient_birth, patient_email=patient_email)
    patient.save()

    return Response(token.key, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def signin(request):
    '''
    로그인
    params: patient_name, patient_password
    return: token 값 (String 형식으로), 200(SUCESS) # 실패에 대한 경우도 생각해야 합니다.
    '''
    patient_name = request.data['patient_name']
    patient_password = request.data['patient_password']

    user = authenticate(username=patient_name, password=patient_password)
    if user is None:
        return Response(status=status.HTTP_401_UNAUTHORIZED) # 권한 없음
    try:
        # user를 통해 token get
        token = Token.objects.get(user=user)
    except:
        # [FIX]: token이 없는 경우 (token 생성 이후 기간이 지나 token이 만료되어 사라진 경우) token 재생성
        token = Token.objects.create(user=user)
    return Response(token.key, status=status.HTTP_200_OK)
    

