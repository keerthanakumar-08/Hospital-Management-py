from django.db import models
from django.utils import timezone

class TimeStampedModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Doctor(TimeStampedModel):     
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Patient(TimeStampedModel):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Appointment(TimeStampedModel):
    doctor = models.ManyToManyField(Doctor)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField(default=timezone.now)
    reason_for_visit = models.TextField()

    def __str__(self):
        return f"Appointment for {self.patient} with {', '.join([str(doc) for doc in self.doctor.all()])} on {self.appointment_date}"
