# Generated by Django 4.2 on 2023-04-05 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizationeventschedule',
            name='scheduleAt',
            field=models.DateField(),
        ),
    ]
