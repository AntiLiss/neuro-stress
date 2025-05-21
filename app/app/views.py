from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin)
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import (Company, CompanyReport, Department, DepartmentReport,
                     EEGRecord, Employee, EmployeeReport)
from .serializers import (CompanyReportSerializer, CompanySerializer,
                          DepartmentReportSerializer, DepartmentSerializer,
                          EEGRecordSerializer, EmployeeReportSerializer,
                          EmployeeSerializer, UserSerializer)
from .services import ReportService


class UserRegisterView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = []


class UserRUDView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["company"]


class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filterset_fields = ["department"]


class EEGRecordViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = EEGRecord.objects.all()
    serializer_class = EEGRecordSerializer
    filterset_fields = ["employee"]


class BaseReportViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    pass


class CompanyReportViewSet(BaseReportViewSet):
    queryset = CompanyReport.objects.all()
    serializer_class = CompanyReportSerializer
    filterset_fields = ["company"]

    def perform_create(self, serializer):
        company = serializer.validated_data.get("company")
        employee_ids = Employee.objects.filter(department__company=company).values_list(
            "id", flat=True
        )

        avg_indexes = ReportService().aggregate_indexes(employee_ids)
        serializer.save(company=company, **avg_indexes)


class DepartmentReportViewSet(BaseReportViewSet):
    queryset = DepartmentReport.objects.all()
    serializer_class = DepartmentReportSerializer
    filterset_fields = ["department"]

    def perform_create(self, serializer):
        department = serializer.validated_data.get("department")
        employee_ids = Employee.objects.filter(department=department).values_list(
            "id", flat=True
        )
        avg_indexes = ReportService().aggregate_indexes(employee_ids)
        serializer.save(department=department, **avg_indexes)


class EmployeeReportViewSet(BaseReportViewSet):
    queryset = EmployeeReport.objects.all()
    serializer_class = EmployeeReportSerializer
    filterset_fields = ["employee"]

    def perform_create(self, serializer):
        employee = serializer.validated_data.get("employee")
        eeg_record = EEGRecord.objects.filter(employee=employee).order_by("-id").first()
        indexes = ReportService().calc_indexes(eeg_record.channel_data)
        serializer.save(employee=employee, **indexes)
