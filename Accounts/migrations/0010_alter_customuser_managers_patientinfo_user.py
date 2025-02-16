# Generated by Django 5.1.6 on 2025-02-15 15:13

import django.contrib.auth.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0009_soulstretch_video_sweatspot_image_sweatspot_video'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customuser',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='patientinfo',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='patient_info', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
