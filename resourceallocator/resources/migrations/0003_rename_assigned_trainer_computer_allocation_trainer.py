# Generated by Django 4.2.1 on 2023-07-17 09:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0002_room_allocation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='computer_allocation',
            old_name='Assigned_Trainer',
            new_name='Trainer',
        ),
    ]
