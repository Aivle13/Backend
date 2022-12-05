from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from user.models import User
# Create your views here.

# 회원가입
@api_view(['POST'])
def signup(request):
    id = request.data['id']
    password = request.data['password']
    
    # 일단 아이디 중복확인은 여기에 로직으로 두었습니다!
    duplicate_user = User.objects.filter(user_id=id)
    if len(duplicate_user) == 0:
        user = User(user_id=id, password=password)
        user.save()
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 로그인
@api_view(['POST'])
def signin(request):
    id = request.data['id']
    password = request.data['password']
    try:
        user = User.objects.get(user_id=id, password=password)
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


# 아이디 중복확인
# @api_view(['POST'])
# def duplicationcheck(request):
#     id = request.data['id']
#     try:
#         user = User.objects.get(user_id=id)
#         return Response('duplication!!!')
#     except:
#         return Response('ok')
