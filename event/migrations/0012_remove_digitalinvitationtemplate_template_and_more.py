# Generated by Django 4.1.7 on 2023-03-25 09:13

from django.db import migrations, models
import event.models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0011_remove_eventinvitationtemplate_htmlfilename_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='digitalinvitationtemplate',
            name='template',
        ),
        migrations.AddField(
            model_name='digitalinvitationtemplate',
            name='htmlFile',
            field=models.FileField(default=1, upload_to=event.models.get_digital_invitation_template_path),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='digitalinvitationtemplate',
            name='templateName',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='digitalinvitationtemplate',
            name='templateOverview',
            field=models.ImageField(default=1, upload_to='eventtemplates/digitalinvitationtemplateoverview'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='eventinvitationtemplate',
            name='templateOverview',
            field=models.ImageField(upload_to='eventtemplates/invitationtemplateoverview'),
        ),
        migrations.AlterField(
            model_name='eventwebpagetemplate',
            name='templateOverview',
            field=models.ImageField(upload_to='eventtemplates/webtemplateoverview'),
        ),
    ]
