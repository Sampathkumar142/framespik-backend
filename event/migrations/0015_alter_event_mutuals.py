# Generated by Django 4.1.7 on 2023-03-26 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_adminpcloudcredential'),
        ('event', '0014_alter_album_event_alter_digitalinvitation_log_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='mutuals',
            field=models.ManyToManyField(blank=True, null=True, related_name='mutualEvents', to='users.customer'),
        ),
    ]