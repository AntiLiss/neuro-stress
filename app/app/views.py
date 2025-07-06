from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
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

    @extend_schema(summary="Создать пользователя")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserRUDView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    @extend_schema(summary="Получить свой профиль")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Частично обновить свой профиль")
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(summary="Полностью обновить свой профиль")
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(summary="Удалить свой профиль")
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


@extend_schema_view(
    list=extend_schema(summary="Получить список всех компаний"),
    retrieve=extend_schema(summary="Получить конкретную компанию"),
    create=extend_schema(summary="Создать компанию"),
    update=extend_schema(summary="Полностью обновить компанию"),
    partial_update=extend_schema(summary="Частично обновить компанию"),
    destroy=extend_schema(summary="Удалить компанию"),
)
class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


@extend_schema_view(
    list=extend_schema(summary="Получить список всех отделов"),
    retrieve=extend_schema(summary="Получить конкретный отдел"),
    create=extend_schema(summary="Создать отдел"),
    update=extend_schema(summary="Полностью обновить отдел"),
    partial_update=extend_schema(summary="Частично обновить отдел"),
    destroy=extend_schema(summary="Удалить отдел"),
)
class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["company"]


@extend_schema_view(
    list=extend_schema(summary="Получить список всех сотрудников"),
    retrieve=extend_schema(summary="Получить конкретного сотрудника"),
    create=extend_schema(summary="Создать сотрудника"),
    update=extend_schema(summary="Полностью обновить сотрудника"),
    partial_update=extend_schema(summary="Частично обновить сотрудника"),
    destroy=extend_schema(summary="Удалить сотрудника"),
)
class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filterset_fields = ["department"]


@extend_schema_view(
    list=extend_schema(summary="Получить список всех записей ЭЭГ"),
    retrieve=extend_schema(summary="Получить конкретную запись ЭЭГ"),
    create=extend_schema(summary="Создать запись ЭЭГ"),
    destroy=extend_schema(summary="Удалить запись ЭЭГ"),
)
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


@extend_schema_view(
    list=extend_schema(summary="Получить список отчетов для всех компаний"),
    retrieve=extend_schema(summary="Получить отчет для конкретной компании"),
    create=extend_schema(summary="Создать отчет для компании"),
    destroy=extend_schema(summary="Удалить отчет компании"),
)
class CompanyReportViewSet(BaseReportViewSet):
    queryset = CompanyReport.objects.all()
    serializer_class = CompanyReportSerializer
    filterset_fields = ["company"]

    def perform_create(self, serializer):
        company = serializer.validated_data.get("company")
        employee_ids = (
            Employee.objects.filter(department__company=company)
            .values_list("id", flat=True)
            .distinct()
        )

        avg_indexes = ReportService().aggregate_indexes(employee_ids)
        serializer.save(company=company, **avg_indexes)


@extend_schema_view(
    list=extend_schema(summary="Получить список отчетов для всех отделов"),
    retrieve=extend_schema(summary="Получить отчет для конкретного отдела"),
    create=extend_schema(summary="Создать отчет для отдела"),
    destroy=extend_schema(summary="Удалить отчет отдела"),
)
class DepartmentReportViewSet(BaseReportViewSet):
    queryset = DepartmentReport.objects.all()
    serializer_class = DepartmentReportSerializer
    filterset_fields = ["department"]

    def perform_create(self, serializer):
        department = serializer.validated_data.get("department")
        employee_ids = (
            Employee.objects.filter(department=department)
            .values_list("id", flat=True)
            .distinct()
        )
        avg_indexes = ReportService().aggregate_indexes(employee_ids)
        serializer.save(department=department, **avg_indexes)


@extend_schema_view(
    list=extend_schema(summary="Получить список отчетов для всех сотрудников"),
    retrieve=extend_schema(summary="Получить отчет для конкретного сотрудника"),
    create=extend_schema(summary="Создать отчет для сотрудника"),
    destroy=extend_schema(summary="Удалить отчет сотрудника"),
)
class EmployeeReportViewSet(BaseReportViewSet):
    queryset = EmployeeReport.objects.all()
    serializer_class = EmployeeReportSerializer
    filterset_fields = ["employee"]

    def perform_create(self, serializer):
        employee = serializer.validated_data.get("employee")
        eeg_record = (
            EEGRecord.objects.filter(employee=employee)
            .order_by("-id")
            .first()
        )
        indexes = ReportService().calc_indexes(eeg_record.channel_data)
        serializer.save(employee=employee, **indexes)
