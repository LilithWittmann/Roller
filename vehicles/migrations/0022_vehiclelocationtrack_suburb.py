# Generated by Django 2.2.3 on 2019-07-14 08:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0021_auto_20190714_0736'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehiclelocationtrack',
            name='suburb',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tracks', to='vehicles.SubUrb'),
        ),
    ]
