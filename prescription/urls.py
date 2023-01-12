from django.urls import path
from .views import homepage,uploadPrescription,viewPrescription,Prescriptions, singleView, annotatePrescription, addAnnotation, predictPrescription, visualizeAnnotation,addMedication, deletePrescription,viewApproval,processApproval, updateApproval,dashboard, customerView, customerUploadForm

urlpatterns = [
    path('', homepage, name="home"),
    path('uploadPrescription/',uploadPrescription,name = 'upload'),
    path('viewPrescription/',viewPrescription,name = 'prescriptions'),
    path('deletePrescription/<int:prescription_id>/', deletePrescription, name = 'deletePrescription'),
    path('prescriptions/',Prescriptions,name = 'Viewprescriptions'),
    # path('dashboard/',Dashboard, name = 'Dashboard'),
    path('singleViewPrescription/<int:prescription_id>/', singleView, name='singleViewPres'),
    path('annotatePrescription/<int:prescription_id>/', annotatePrescription, name='annotatePrescription'),
    path('predictPrescription/<int:prescription_id>/', predictPrescription, name='predictPrescription'),
    path('addMedication/<int:prescription_id>/', addMedication, name='addMedication'),
    path('addAnnotation/<int:prescription_id>/', addAnnotation),
    path('visualiseAnnotation/<int:prescription_id>/', visualizeAnnotation, name='visualise'),
    path('viewApproval/',viewApproval,name = 'approvals'),
    path('processApproval/<int:prescription_id>/',processApproval, name='processApproval'),
    path('updateApproval/<int:prescription_id>/',updateApproval, name='updateApproval'),
    path('dashboard/',dashboard,name="dashboard"),
    path('uploadCustomer/',customerView, name = "customerView"),
    path('uploadCustomerForm/',customerUploadForm, name = "customerUploadForm")
]