from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Prescription(models.Model):
    uploaded_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    uploaded_on = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to = 'uploadedPrescriptions/')
    annotation = models.JSONField(null=True, blank=True)
    medication = models.JSONField(null=True,blank=True)
    digitzedImagePdf = models.FileField(upload_to = 'DigitizedPrescriptionImage_pdf/')
    digitzedPdf = models.FileField(upload_to = 'DigitizedPrescription_pdf/')