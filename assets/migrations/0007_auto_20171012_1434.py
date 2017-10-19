# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-12 06:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0006_auto_20170907_0940'),
    ]

    operations = [
        migrations.AddField(
            model_name='hardwareasset',
            name='service_request_url',
            field=models.URLField(blank=True, max_length=2000, null=True, verbose_name='Service request URL', help_text='URL (e.g. Freshdesk, Jira, etc.) of the service request for purchase of this asset.'),
        ),
        migrations.AddField(
            model_name='softwareasset',
            name='service_request_url',
            field=models.URLField(blank=True, max_length=2000, null=True, verbose_name='Service request URL', help_text='URL (e.g. Freshdesk, Jira, etc.) of the service request for purchase of this asset.'),
        ),
    ]
