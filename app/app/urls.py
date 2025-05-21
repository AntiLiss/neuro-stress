from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import (CompanyReportViewSet, CompanyViewSet,
                    DepartmentReportViewSet, DepartmentViewSet,
                    EEGRecordViewSet, EmployeeReportViewSet, EmployeeViewSet,
                    UserRegisterView, UserRUDView)

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
    path("register/", UserRegisterView.as_view(), name="register"),
    path("me/", UserRUDView.as_view(), name="me"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
