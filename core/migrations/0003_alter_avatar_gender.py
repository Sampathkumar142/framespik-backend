# Generated by Django 4.1.7 on 2023-03-19 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_avatar_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avatar',
            name='gender',
            field=models.CharField(choices=[('O', 'Other'), ('M', 'Male'), ('F', 'Female')], max_length=1),
        ),
    ]
