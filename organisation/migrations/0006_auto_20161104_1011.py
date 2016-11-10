# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-11-04 02:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0005_auto_20161103_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departmentuser',
            name='org_unit',
            field=models.ForeignKey(blank=True, help_text="The organisational unit that represents the user's primary physical location (also set their distribution group).", null=True, on_delete=django.db.models.deletion.PROTECT, to='organisation.OrgUnit', verbose_name='organisational unit'),
        ),
    ]