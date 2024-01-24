# views.py
import os
import random
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework import status, views
from .models import Doctor, Patient, Appointment
from .serializers import DoctorSerializer, PatientSerializer, AppointmentSerializer, LoginSerializer
from twilio.rest import Client 



TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN'),

def send_otp(to, otp):
    # Initialize Twilio client
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    # Send OTP via SMS using Twilio
    message = client.messages.create(
        body=f'Your OTP is: {otp}',
        to=to
    )
    
class LoginView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username_or_email = serializer.validated_data['username_or_email']

        user = Patient.objects.get(email=username_or_email)  # Adjust based on your model
        if user:
            # Generate a 6-digit OTP
            otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])

            # Initialize Twilio client
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

            # Send OTP via SMS using Twilio
            message = client.messages.create(
                body=f'Your OTP is: {otp}',
                to=user.contact_number
            )

            # You may want to save this OTP in the database for verification, if needed

            return JsonResponse({'detail': 'OTP sent successfully.'})
        else:
            return JsonResponse({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


