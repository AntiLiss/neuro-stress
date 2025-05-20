from rest_framework import serializers
from rest_framework.serializers import ValidationError
from .models import (
    EEGRecord,
    Company,
    Department,
    Employee,
    BaseReport,
    CompanyReport,
    DepartmentReport,
    EmployeeReport,
)


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("id", "name", "description")
        read_only_fields = ("id",)


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ("id", "name", "description", "company")
        read_only_fields = ("id",)


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ("id", "first_name", "last_name", "middle_name", "department")
        read_only_fields = ("id",)


class EEGRecordSerializer(serializers.ModelSerializer):
    channel_data = serializers.ListField(
        child=serializers.ListField(
            child=serializers.FloatField(),
        )
    )

    class Meta:
        model = EEGRecord
        fields = (
            "id",
            "channel_data",  # Фронт должен отправлять только данные каналов!
            "employee",
        )

    def validate_channel_data(self, value):
        if len(value) != 6:
            raise ValidationError("Ожидалось 6 подмассивов!")
        return value


class BaseReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseReport
        fields = (
            "id",
            "valence",
            "arousal",
            "relaxation",
            "drowsiness",
            "stress",
            "concentration",
        )
        read_only_fields = fields

    def get_eeg_filter(self, attrs):
        pass

    def validate(self, attrs):
        filter_kwargs = self.get_eeg_filter(attrs)
        if not EEGRecord.objects.filter(**filter_kwargs).exists():
            raise ValidationError("Отсутствуют данные ЭЭГ")
        return attrs


class CompanyReportSerializer(BaseReportSerializer):
    class Meta(BaseReportSerializer.Meta):
        model = CompanyReport
        fields = BaseReportSerializer.Meta.fields + ("company",)

    def get_eeg_filter(self, attrs):
        return {"employee__department__company": attrs["company"]}


class DepartmentReportSerializer(BaseReportSerializer):
    class Meta(BaseReportSerializer.Meta):
        model = DepartmentReport
        fields = BaseReportSerializer.Meta.fields + ("department",)

    def get_eeg_filter(self, attrs):
        return {"employee__department": attrs["department"]}


class EmployeeReportSerializer(BaseReportSerializer):
    class Meta(BaseReportSerializer.Meta):
        model = EmployeeReport
        fields = BaseReportSerializer.Meta.fields + ("employee",)

    def get_eeg_filter(self, attrs):
        return {"employee": attrs["employee"]}
