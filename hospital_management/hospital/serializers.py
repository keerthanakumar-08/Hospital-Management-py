# serializers.py

from rest_framework import serializers
from .models import Doctor, Patient, Appointment

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        email = data.get('email')

        if not email:
            raise serializers.ValidationError('Email is required.')

        # Try to get the user by matching the email
        user = Patient.objects.filter(email=email).first()

        if user:
            data['user'] = user
            return data
        else:
            raise serializers.ValidationError('Invalid email.')
        
                
class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
