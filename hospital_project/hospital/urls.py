from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DoctorViewSet, ServiceViewSet, VisitViewSet, PatientViewSet

router = DefaultRouter()
router.register(r'doctors', DoctorViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'visits', VisitViewSet)
router.register(r'patients', PatientViewSet, basename='patient')

urlpatterns = [
    path('', include(router.urls)),
]