# Generated by Django 2.1.10 on 2019-07-12 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0003_auto_20190712_2043'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehiclelocationtrack',
            name='updated_at',
            field=models.DateTimeField(null=True),
        ),
    ]
