# Generated by Django 4.0.5 on 2022-10-29 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prescription', '0005_prescription_medication'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescription',
            name='digitzedImagePdf',
            field=models.FileField(default='asd', upload_to='DigitizedPrescriptionPdf/'),
            preserve_default=False,
        ),
    ]