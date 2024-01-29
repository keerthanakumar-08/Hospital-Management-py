# views.py
import os
import random
from django.views import View
from rest_framework.views import APIView
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework import status, views
from .models import Doctor, Patient, Appointment
from .serializers import DoctorSerializer, PatientSerializer, AppointmentSerializer, LoginSerializer
from twilio.rest import Client 
from drf_yasg.utils import swagger_auto_schema
import secrets




TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')


# def send_otp(to, otp):
#     # Initialize Twilio client
#     client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

#     from_phone_number = '59039149'  # Replace with your Twilio trial phone number
#     message = client.messages.create(
#         body=f'Your OTP is: {otp}',
#         to='+919500763210',
#         from_=from_phone_number
#     )
    
class LoginView(APIView):
    serializer_class = LoginSerializer

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']  # Use 'email' instead of 'username_or_email'

        try:
            user = Patient.objects.get(email=email)
        except Patient.DoesNotExist:
            return JsonResponse({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

        if user:
            # Generate a 6-digit OTP
            otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])

            # Initialize Twilio client
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            from_phone_number = os.environ.get('TWILIO_PHONE_NO')

            # Send OTP via SMS using Twilio
            message = client.messages.create(
                body=f'Your OTP is: {otp}',
                to='+919500763210',
                from_=from_phone_number
            )

            # Store OTP in the user's session or any temporary storage for verification
            request.session['otp'] = otp
            request.session['user_id'] = user.id

            return JsonResponse({'detail': 'OTP sent successfully.'})
        else:
            return JsonResponse({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)


class OTPVerificationView(View):
    def post(self, request, *args, **kwargs):
        otp_entered = request.POST.get('otp')
        user_id = request.session.get('user_id')
        stored_otp = request.session.get('otp')

        if otp_entered == stored_otp:
            # OTP is correct, you can proceed with login or any other action
            # Clear OTP from session
            del request.session['otp']
            del request.session['user_id']
            return JsonResponse({'detail': 'OTP verification successful.'})
        else:
            return JsonResponse({'detail': 'Invalid OTP.'}, status=status.HTTP_401_UNAUTHORIZED)

class DoctorViewSet(viewsets.ModelViewSet): 
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


