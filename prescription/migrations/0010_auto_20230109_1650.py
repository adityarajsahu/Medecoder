# Generated by Django 3.2.16 on 2023-01-09 11:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prescription', '0009_prescription_filename'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prescription',
            name='fileName',
        ),
        migrations.AlterField(
            model_name='approval',
            name='prescription',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='prescription.prescription'),
        ),
    ]
