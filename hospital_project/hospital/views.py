
from rest_framework import mixins, viewsets, filters, permissions
from .serializers import ServiceSerializer
from .serializers import VisitSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import DoctorSerializer, PatientSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsDoctor
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from django.db.models import Count, Avg, F, ExpressionWrapper, DurationField
from .models import Patient, Doctor, Visit, Service, Feedback, FinancialRecord


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

class AnalyticsView(APIView):
    permission_classes = [IsAdminUser]  # Только админы могут видеть панель

    def get(self, request):
        total_patients = Patient.objects.count()
        total_doctors = Doctor.objects.count()

        average_wait_time = Visit.objects.aggregate(avg_wait=Avg('date'))  # Пример — нужно уточнить
        average_treatment_time = Visit.objects.aggregate(avg_treat=Avg('services__cost'))  # Пример
        patient_satisfaction = Feedback.objects.aggregate(avg_rating=Avg('rating'))  # Оценка 1–5

        total_income = FinancialRecord.objects.filter(type='income').aggregate(total=Sum('amount'))['total'] or 0
        total_expenses = FinancialRecord.objects.filter(type='expense').aggregate(total=Sum('amount'))['total'] or 0
        profit = total_income - total_expenses

        return Response({
            "total_patients": total_patients,
            "total_doctors": total_doctors,
            "average_wait_time": average_wait_time['avg_wait'],
            "average_treatment_cost": average_treatment_time['avg_treat'],
            "patient_satisfaction": patient_satisfaction['avg_rating'],
            "financials": {
                "income": total_income,
                "expenses": total_expenses,
                "profit": profit
            }
        })
