# Generated by Django 5.0.2 on 2024-03-13 16:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0004_remove_etage_numetage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='zone',
            old_name='typelocal',
            new_name='typeLocal',
        ),
    ]
