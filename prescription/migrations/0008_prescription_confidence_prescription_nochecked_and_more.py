# Generated by Django 4.1.3 on 2023-01-06 07:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('prescription', '0007_prescription_digitzedpdf_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescription',
            name='confidence',
            field=models.FloatField(default=1),
        ),
        migrations.AddField(
            model_name='prescription',
            name='noChecked',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Approval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='Pending', max_length=20)),
                ('checkedBy', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('prescription', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='prescription.prescription')),
            ],
        ),
    ]
