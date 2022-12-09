from django.db import models
from django.conf import settings

# Create your models here.
class Patient (models.Model):

    # Login 기능 시 Token을 만들기 위해 필요합니다.
    # 기본적인 보안을 제공하는 AUTH_USER_MODEL을 1대 1로 매핑한 관계입니다.
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+', on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=10, default='')
    patient_birth = models.DateField(default='') 
    patient_phone_number = models.CharField(max_length=20, default='')
    patient_email = models.CharField(max_length=50, null=True, blank=True) # null=True, blank=True: DB에서 NULL 허용
    