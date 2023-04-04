# Generated by Django 4.1.7 on 2023-04-01 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_alter_avatar_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avatar',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('O', 'Other'), ('F', 'Female')], max_length=1),
        ),
    ]
