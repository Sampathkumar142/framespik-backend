# Generated by Django 4.1.7 on 2023-03-25 06:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0008_albumface'),
    ]

    operations = [
        migrations.RenameField(
            model_name='albumface',
            old_name='face_url',
            new_name='faceUrl',
        ),
    ]
