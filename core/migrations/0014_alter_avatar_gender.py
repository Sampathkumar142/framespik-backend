# Generated by Django 4.1.7 on 2023-03-25 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_alter_avatar_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avatar',
            name='gender',
            field=models.CharField(choices=[('O', 'Other'), ('F', 'Female'), ('M', 'Male')], max_length=1),
        ),
    ]