# Generated by Django 4.1.7 on 2023-04-03 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_alter_avatar_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avatar',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('O', 'Other'), ('F', 'Female')], max_length=1),
        ),
    ]
