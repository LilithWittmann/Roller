# Generated by Django 2.2.3 on 2019-07-14 07:34

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0019_auto_20190714_0730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suburb',
            name='area',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326),
        ),
    ]
