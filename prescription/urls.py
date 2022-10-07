from django.urls import path
from .views import homepage,uploadPrescription,viewPrescription,Prescriptions,Dashboard, singleView

urlpatterns = [
    path('', homepage, name="home"),
    path('uploadPrescription/',uploadPrescription,name = 'upload'),
    path('viewPrescription/',viewPrescription,name = 'prescriptions'),
    path('prescriptions/',Prescriptions,name = 'Viewprescriptions'),
    path('dashboard/',Dashboard, name = 'Dashboard'),
    path('singleViewPrescription/<int:prescription_id>/', singleView, name='singleViewPres'),
]