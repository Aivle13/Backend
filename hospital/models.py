from django.db import models
from django.conf import settings

# Create your models here.
class Hospital(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+', on_delete=models.CASCADE, null=True)
    hospital_name = models.CharField(max_length=50, default='')
    hospital_address = models.CharField(max_length=50, default='') #필수로 입력해야 될 것 같다
    hospital_phone_number = models.CharField(max_length=20, null=True, blank=True) # null=True, blank=True: DB에서 NULL 허용
    hospital_department = models.CharField(max_length=10, default='')