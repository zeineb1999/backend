# Generated by Django 5.0.2 on 2024-03-24 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0011_etage_nometage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='etage',
            name='surface',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
