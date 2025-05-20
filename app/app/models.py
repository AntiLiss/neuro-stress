from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)


class Department(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)


class Employee(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)


class EEGRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    channel_data = models.JSONField(default=list)


class BaseReport(models.Model):
    valence = models.FloatField()
    arousal = models.FloatField()
    relaxation = models.FloatField()
    drowsiness = models.FloatField()
    stress = models.FloatField()
    concentration = models.FloatField()

    class Meta:
        abstract = True


class CompanyReport(BaseReport):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


class DepartmentReport(BaseReport):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)


class EmployeeReport(BaseReport):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
