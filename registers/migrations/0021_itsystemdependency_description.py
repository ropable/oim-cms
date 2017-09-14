# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-14 02:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registers', '0020_auto_20170713_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='itsystemdependency',
            name='description',
            field=models.TextField(blank=True, help_text='Details of the dependency, its criticality, any workarounds, etc.', null=True),
        ),
    ]
