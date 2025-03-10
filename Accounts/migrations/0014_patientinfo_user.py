# Generated by Django 5.1.6 on 2025-02-15 16:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0013_remove_patientinfo_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientinfo',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='patient_info', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
