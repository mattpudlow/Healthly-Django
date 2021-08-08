from django.contrib import admin
from .models import HospitalData, CostData, Procedure

# Register your models here.
admin.site.register(CostData)
admin.site.register(HospitalData)
admin.site.register(Procedure)