# Generated by Django 4.1.7 on 2023-03-19 15:12

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomFeaturePlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('htmlId', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='FeatureCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='FeaturePlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=80)),
                ('pcloudImageID', models.CharField(max_length=100)),
                ('pcloudPublicCode', models.CharField(max_length=1000)),
                ('proprietorImageUrl', models.URLField(blank=True, null=True)),
                ('address', models.TextField()),
                ('isMaintainingOffice', models.BooleanField()),
                ('latitude', models.CharField(max_length=30)),
                ('longitude', models.CharField(max_length=30)),
                ('whatsapp', models.CharField(max_length=10)),
                ('phoneNumber', models.CharField(max_length=13)),
                ('facebook', models.TextField(blank=True, null=True)),
                ('instagram', models.TextField(blank=True, null=True)),
                ('youtube', models.TextField(blank=True, null=True)),
                ('albumsCount', models.PositiveBigIntegerField(default=0)),
                ('eventsCount', models.PositiveBigIntegerField(default=0)),
                ('invitationsCount', models.PositiveBigIntegerField(default=0)),
                ('streamsCount', models.PositiveBigIntegerField(default=0)),
                ('emiPayable', models.BooleanField(default=False)),
                ('isCustomPlan', models.BooleanField(default=False)),
                ('bankAccountNumber', models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator('^[0-9]{9,18}$', 'Invalid bank account number'), django.core.validators.MinLengthValidator(9), django.core.validators.MaxLengthValidator(18)])),
                ('ifscCode', models.CharField(blank=True, max_length=11, null=True, validators=[django.core.validators.RegexValidator('^[A-Z]{4}[0-9]{7}$', 'Invalid IFSC code')])),
                ('nameAsPerBank', models.CharField(blank=True, max_length=255, null=True)),
                ('bankName', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(choices=[('A', 'Active'), ('H', 'Hold'), ('I', 'In Active')], default='A', max_length=1)),
                ('lastUpdated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isFaceRecognitionEnable', models.BooleanField()),
                ('isProductionToolsEnable', models.BooleanField()),
                ('title', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationEcardTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('htmlFileName', models.CharField(max_length=1000)),
                ('pcloudImageID', models.CharField(max_length=100)),
                ('pcloudPublicCode', models.CharField(max_length=1000)),
                ('templateName', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationEventCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('isFaceRecognitionEnable', models.BooleanField()),
                ('thumbnail', models.URLField(unique=True)),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationTier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avgQuotation', models.BigIntegerField()),
                ('title', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationWebpageTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('htmlFileName', models.CharField(max_length=1000)),
                ('pcloudImageID', models.CharField(max_length=100)),
                ('pcloudPublicCode', models.CharField(max_length=1000)),
                ('templateName', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PcloudAccountPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('tenure', models.IntegerField()),
                ('storage', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationWebpage',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('isActive', models.BooleanField(default=True)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.organization')),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='organization.organizationwebpagetemplate')),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationViews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('webViews', models.PositiveBigIntegerField(default=0)),
                ('appViews', models.PositiveBigIntegerField(default=0)),
                ('promotionalViews', models.PositiveBigIntegerField(default=0)),
                ('organization', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='views', to='organization.organization')),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationPortfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thumb', models.URLField(unique=True)),
                ('pcloudImageID', models.CharField(max_length=100)),
                ('pcloudPublicCode', models.CharField(max_length=3000)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='organization.organizationeventcategory')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.organization')),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationPcloudCredentials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=150)),
                ('auth', models.CharField(blank=True, max_length=225, null=True)),
                ('nextRenewableDate', models.DateField(blank=True, null=True)),
                ('lastLogin', models.DateField(blank=True, default='2023-03-01', null=True)),
                ('organization', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='credential', to='organization.organization')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='organization.pcloudaccountplan')),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationNormalShedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('createdAt', models.DateTimeField(auto_now=True)),
                ('sheduledAt', models.DateTimeField()),
                ('status', models.BooleanField(default=False)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.organization')),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationEcard',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('isActive', models.BooleanField(default=True)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.organization')),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='organization.organizationecardtemplate')),
            ],
        ),
        migrations.AddField(
            model_name='organization',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='organization.organizationcategory'),
        ),
        migrations.AddField(
            model_name='organization',
            name='plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='organization.featureplan'),
        ),
    ]
