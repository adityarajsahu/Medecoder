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

    noChecked = models.IntegerField(default=0)
    confidence = models.FloatField(default=1)

class Approval(models.Model):
    status = models.CharField(default="Pending",max_length=20)
    prescription = models.ForeignKey(Prescription,null = True, on_delete=models.CASCADE)
    checkedBy = models.ForeignKey(User,null=True, on_delete=models.SET_NULL)


class CustomerPrescription(models.Model):
    image = models.ImageField(upload_to = 'customerUploadedPrescriptions/')
    annotation = models.JSONField(null=True, blank=True)
    medication = models.JSONField(null=True,blank=True)
    uploaded_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    phoneNumber = models.IntegerField(default=9937097399)

