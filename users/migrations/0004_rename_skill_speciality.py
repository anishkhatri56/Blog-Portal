# Generated by Django 4.0.4 on 2022-08-06 16:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_location_skill'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Skill',
            new_name='Speciality',
        ),
    ]
