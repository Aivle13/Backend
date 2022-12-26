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
from django.core import serializers

# Model (CRUD 대상)
from patient.models import Patient
from hospital.models import Hospital

@api_view(['POST'])
def signup(request):
    '''
    회원가입
    params: patient_name, patient_password, patient_birth, patient_email
    return: 201(SUCESS) # 실패에 대한 경우도 생각해야 합니다.
    '''
    patient_userid = request.data['patient_userid']
    patient_password = request.data['patient_password']

    user = User.objects.create_user(username=patient_userid, password=patient_password)
    token = Token.objects.create(user=user) # 토근 생성
    user.save() # AUTH_USER_MODEL의 User 저장
    
    patient_name = request.data['patient_name']
    patient_birth = request.data['patient_birth']
    patient_phone_number = request.data['patient_phone_number']
    patient_email = request.data['patient_email']

    patient = Patient(author = user,
                      patient_name = patient_name,
                      patient_birth = patient_birth, 
                      patient_phone_number = patient_phone_number,
                      patient_email = patient_email)
    patient.save()

    return Response(token.key, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def signin(request):
    '''
    로그인
    params: patient_name, patient_password
    return: token 값 (String 형식으로), 200(SUCESS) # 실패에 대한 경우도 생각해야 합니다.
    '''
    patient_name = request.data['patient_userid']
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

    
@api_view(['POST'])
def hospital_srch(request):

   hospital_dep = request.data['hospitalDep']
   hospitals = serializers.serialize("json", Hospital.objects.filter(hospital_department=hospital_dep))
   
   return Response(hospitals, status=status.HTTP_200_OK)
    

@api_view(['PUT','POST'])
def mypage(request):
    if request.method == 'POST':
        user = request.user
        patient = Patient.objects.get(author=user.id)
        data = {
            'id' : user.username,
            'name' : patient.patient_name,
            'birth' : patient.patient_birth,
            'phone' : patient.patient_phone_number,
            'email' : patient.patient_email,
        }
        return Response(data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        user = request.user # token을 통해서 user를 가져옴
        patient = Patient.objects.get(author=user.id)
        user.set_password(request.data['patient_password'])
        user.save()
        patient.patient_name = request.data['patient_name']
        patient.patient_birth = request.data['patient_birth']
        patient.patient_phone_number = request.data['patient_phone_number']
        patient.patient_email = request.data['patient_email']
        
        patient.save()
        
        return Response(status=status.HTTP_200_OK)