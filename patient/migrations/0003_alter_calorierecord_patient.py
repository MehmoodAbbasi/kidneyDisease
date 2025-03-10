# Generated by Django 5.1.6 on 2025-03-07 11:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0002_soulstretch_patient_sweatspot_patient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calorierecord',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='calorie_records', to='patient.patient'),
        ),
    ]
