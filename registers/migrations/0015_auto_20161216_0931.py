# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-12-16 01:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registers', '0014_delete_software'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itsystemhardware',
            name='computer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tracking.Computer'),
        ),
    ]