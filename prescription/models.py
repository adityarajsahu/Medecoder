from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Prescription(models.Model):
    uploaded_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    uploaded_on = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to = 'uploadedPrescriptions/')