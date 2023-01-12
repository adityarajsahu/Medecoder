from django.contrib import admin
from .models import Prescription,Approval, CustomerPrescription
# Register your models here.

admin.site.register(Prescription)
admin.site.register(Approval)
admin.site.register(CustomerPrescription)

