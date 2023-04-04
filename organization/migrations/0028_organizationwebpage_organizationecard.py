# Generated by Django 4.1.7 on 2023-03-30 13:54

from django.db import migrations, models
import django.db.models.deletion
import organization.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0027_remove_organizationwebpage_organization_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationWebpage',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('isActive', models.BooleanField(default=True)),
                ('isPublic', models.BooleanField(default=True)),
                ('passCode', models.CharField(default=organization.models.generate_unique_string_webpage, max_length=8, unique=True)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.organization')),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='organization.organizationwebpagetemplate')),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationEcard',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('isActive', models.BooleanField(default=True)),
                ('passCode', models.CharField(default=organization.models.generate_unique_string_ecard, max_length=8, unique=True)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.organization')),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='organization.organizationecardtemplate')),
            ],
        ),
    ]