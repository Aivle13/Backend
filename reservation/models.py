from django.db import models
from patient.models import Patient
from hospital.models import Hospital

# Create your models here.
class Reservation(models.Model):
    STATE = (
        ('P','PENDING AOOROVED'),
        ('A', 'APPROVED'),
        ('R', 'REJECTED'),
        ('C', 'COMPLETE'),
    )
    reservation_time = models.DateTimeField(auto_now_add=True)
    reservation_comment = models.TextField()
    # reservation_state = models.TextChoices("reservation_state",'PENDING AOOROVED COMApproved Rejected complete')
    reservation_state = models.CharField(max_length=1, choices=STATE, default='P')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)