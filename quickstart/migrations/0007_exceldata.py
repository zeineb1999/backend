# Generated by Django 5.0.2 on 2024-03-20 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0006_zone_surface'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExcelData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('column1', models.FloatField()),
                ('column2', models.FloatField()),
            ],
        ),
    ]
