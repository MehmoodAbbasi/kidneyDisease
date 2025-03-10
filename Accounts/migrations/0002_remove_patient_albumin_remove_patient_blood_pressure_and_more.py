# Generated by Django 5.1.6 on 2025-02-11 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='albumin',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='blood_pressure',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='hemoglobin',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='potassium',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='sodium',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='sugar',
        ),
        migrations.AddField(
            model_name='patient',
            name='al',
            field=models.FloatField(default=1, verbose_name='Albumin'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='ane',
            field=models.CharField(default=1, max_length=3, verbose_name='Anemia'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='appet',
            field=models.CharField(default=1, max_length=10, verbose_name='Appetite'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='ba',
            field=models.CharField(default=1, max_length=10, verbose_name='Bacteria'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='bgr',
            field=models.FloatField(default=1, verbose_name='Blood Glucose Random'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='bp',
            field=models.FloatField(default=1, verbose_name='Blood Pressure'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='bu',
            field=models.FloatField(default=1, verbose_name='Blood Urea'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='cad',
            field=models.CharField(default=1, max_length=3, verbose_name='Coronary Artery Disease'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='dm',
            field=models.CharField(default=1, max_length=3, verbose_name='Diabetes Mellitus'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='hemo',
            field=models.FloatField(default=1, verbose_name='Hemoglobin'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='htn',
            field=models.CharField(default=1, max_length=3, verbose_name='Hypertension'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='pc',
            field=models.CharField(default=1, max_length=10, verbose_name='Pus Cells'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='pcc',
            field=models.CharField(default=1, max_length=10, verbose_name='Pus Cell Clumps'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='pcv',
            field=models.FloatField(default=1, verbose_name='Packed Cell Volume'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='pe',
            field=models.CharField(default=1, max_length=3, verbose_name='Pedal Edema'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='pot',
            field=models.FloatField(default=1, verbose_name='Potassium'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='rbc',
            field=models.CharField(default=1, max_length=10, verbose_name='Red Blood Cells'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='rc',
            field=models.FloatField(default=1, verbose_name='Red Blood Cell Count'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='sc',
            field=models.FloatField(default=1, verbose_name='Serum Creatinine'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='sg',
            field=models.FloatField(default=1, verbose_name='Specific Gravity'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='sod',
            field=models.FloatField(default=1, verbose_name='Sodium'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='su',
            field=models.FloatField(default=1, verbose_name='Sugar'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='wc',
            field=models.FloatField(default=1, verbose_name='White Blood Cell Count'),
            preserve_default=False,
        ),
    ]
