# Generated by Django 2.2.3 on 2020-03-02 20:22

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0033_auto_20200302_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='tripestimation',
            name='route_timing',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='route timing'),
        ),
    ]