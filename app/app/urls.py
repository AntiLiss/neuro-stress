from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    EEGRecordViewSet,
    CompanyViewSet,
    DepartmentViewSet,
    EmployeeViewSet,
    CompanyReportViewSet,
    DepartmentReportViewSet,
    EmployeeReportViewSet,
)

router = DefaultRouter()
router.register("companies", CompanyViewSet)
router.register("departments", DepartmentViewSet)
router.register("employees", EmployeeViewSet)
router.register("eeg-records", EEGRecordViewSet)

router.register("company-reports", CompanyReportViewSet)
router.register("department-reports", DepartmentReportViewSet)
router.register("employee-reports", EmployeeReportViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
