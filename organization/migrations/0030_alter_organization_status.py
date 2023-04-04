# Generated by Django 4.1.7 on 2023-04-03 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0029_alter_organization_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='status',
            field=models.CharField(choices=[('A', 'Active'), ('I', 'In Active'), ('H', 'Hold')], default='A', max_length=1),
        ),
    ]