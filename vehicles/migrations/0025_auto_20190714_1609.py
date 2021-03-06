# Generated by Django 2.2.3 on 2019-07-14 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0024_auto_20190714_1320'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='tripestimation',
            index=models.Index(fields=['vehicle'], name='vehicles_tr_vehicle_d5f3f7_idx'),
        ),
        migrations.AddIndex(
            model_name='tripestimation',
            index=models.Index(fields=['vehicle', 'updated_at'], name='vehicles_tr_vehicle_9a24dd_idx'),
        ),
        migrations.AddConstraint(
            model_name='tripestimation',
            constraint=models.UniqueConstraint(fields=('start_point',), name='unique-start'),
        ),
        migrations.AddConstraint(
            model_name='tripestimation',
            constraint=models.UniqueConstraint(fields=('end_point',), name='unique-end'),
        ),
    ]
