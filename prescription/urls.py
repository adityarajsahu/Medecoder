from django.urls import path
from .views import homepage,uploadPrescription,viewPrescription,Prescriptions,Dashboard

urlpatterns = [
    path('', homepage, name="home"),
    path('uploadPrescription/',uploadPrescription,name = 'upload'),
    path('viewPrescription/',viewPrescription,name = 'viewPrescription'),
    path('prescriptions/',Prescriptions,name = 'Prescriptions'),
    path('dashboard/',Dashboard, name = 'Dashboard')
]