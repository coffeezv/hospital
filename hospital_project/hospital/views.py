
from rest_framework import mixins, viewsets
from .models import Service
from .serializers import ServiceSerializer
from .models import Visit
from .serializers import VisitSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Doctor, Patient
from .serializers import DoctorSerializer, PatientSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsDoctor
from rest_framework import viewsets, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend

class DoctorViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    @action(detail=True, methods=['get'])
    def patients(self, request, pk=None):
        doctor = self.get_object()
        visits = Visit.objects.filter(doctor=doctor)
        patients = Patient.objects.filter(id__in=visits.values_list('patient_id', flat=True).distinct())
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)


class ServiceViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class VisitViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    permission_classes = [permissions.DjangoModelPermissions]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['date_of_birth', 'phone']
    search_fields = ['name', 'address']
    ordering_fields = ['date_of_birth']
