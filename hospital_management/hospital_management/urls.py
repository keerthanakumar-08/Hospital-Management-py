from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter

from hospital.views import DoctorViewSet, PatientViewSet, AppointmentViewSet, LoginView

router = DefaultRouter()
router.register(r'doctors', DoctorViewSet, basename='doctor')
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'appointments', AppointmentViewSet, basename='appointment')

schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version='v1',
        description="Your API description",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="contact@yourapp.com"),
        license=openapi.License(name="Your License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/login/', LoginView.as_view(), name='login'),  # Register LoginView separately
    # Swagger documentation
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
