# Generated by Django 3.2.5 on 2021-07-30 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='profit',
            field=models.FloatField(default=0),
        ),
    ]
