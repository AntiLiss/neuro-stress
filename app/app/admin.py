from django.contrib import admin

# Register your models here.
from .models import Company, Department, Employee, EEGRecord

admin.site.register(Company)
admin.site.register(Department)
admin.site.register(Employee)
admin.site.register(EEGRecord)
