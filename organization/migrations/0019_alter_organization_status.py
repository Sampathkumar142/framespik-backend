# Generated by Django 4.1.7 on 2023-03-30 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0018_alter_organization_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='status',
            field=models.CharField(choices=[('H', 'Hold'), ('I', 'In Active'), ('A', 'Active')], default='A', max_length=1),
        ),
    ]
