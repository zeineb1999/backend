# Generated by Django 5.0.2 on 2024-03-19 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0005_rename_typelocal_zone_typelocal'),
    ]

    operations = [
        migrations.AddField(
            model_name='zone',
            name='surface',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
