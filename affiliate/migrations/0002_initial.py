# Generated by Django 4.1.7 on 2023-03-19 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organization', '0001_initial'),
        ('affiliate', '0001_initial'),
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizationsettled',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='organization.organization'),
        ),
        migrations.AddField(
            model_name='organizationcommision',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='organization.organization'),
        ),
        migrations.AddField(
            model_name='organizationcommision',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='event.digitalinvitationlog'),
        ),
    ]
