# Generated by Django 2.2.3 on 2019-07-13 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0011_tripestimation_route_estimation'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='vehiclelocationtrack',
            index=models.Index(fields=['vehicle'], name='vehicles_ve_vehicle_519caa_idx'),
        ),
        migrations.AddIndex(
            model_name='vehiclelocationtrack',
            index=models.Index(fields=['vehicle', 'updated_at'], name='vehicles_ve_vehicle_e3cf8f_idx'),
        ),
    ]
