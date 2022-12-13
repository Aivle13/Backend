from django.db import models
from patient.models import Patient
from hospital.models import Hospital

# Create your models here.
class Reservation(models.Model):

    reservation_time = models.DateTimeField(auto_now_add=True)
    reservation_comment = models.TextField()

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
