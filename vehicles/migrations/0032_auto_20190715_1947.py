# Generated by Django 2.2.3 on 2019-07-15 19:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0031_auto_20190715_1835'),
    ]

    operations = [
        migrations.AddField(
            model_name='tripestimation',
            name='ended_at_station',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ended_trips', to='vehicles.PublicTransportStation'),
        ),
        migrations.AddField(
            model_name='tripestimation',
            name='started_at_station',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='started_trips', to='vehicles.PublicTransportStation'),
        ),
    ]
