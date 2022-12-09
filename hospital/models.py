from django.db import models

# Create your models here.
class Hospital(models.Model):

    hospital_name = models.CharField(max_length=50)
    hospital_address = models.CharField(max_length=50, null=True, blank=True) # null=True, blank=True: DB에서 NULL 허용
    hospital_phone_number = models.CharField(max_length=20, null=True, blank=True) # null=True, blank=True: DB에서 NULL 허용
    hospital_department = models.CharField(max_length=10)