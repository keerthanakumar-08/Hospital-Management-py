# hospital/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DoctorViewSet, LoginView, PatientViewSet, AppointmentViewSet

router = DefaultRouter()
router.register(r'doctors', DoctorViewSet, basename='doctor')
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r'login', LoginView.as_view(),basename='login')

urlpatterns = [
    path('', include(router.urls)),
    # path('login/', LoginView.as_view(), name='login'),
]
