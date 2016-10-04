# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-03 14:17
from __future__ import unicode_literals

from django.db import migrations, models
import registers.models


class Migration(migrations.Migration):

    dependencies = [
        ('registers', '0002_auto_20160919_1303'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='processitsystemrelationship',
            options={'verbose_name_plural': 'Process/IT System relationships'},
        ),
        migrations.AddField(
            model_name='itsystem',
            name='alt_processing',
            field=models.TextField(blank=True, null=True, verbose_name='alternate processing procedure'),
        ),
        migrations.AddField(
            model_name='itsystem',
            name='capability',
            field=registers.models.ChoiceArrayField(base_field=models.CharField(choices=[('0', 'Information lifecycle'), ('1', 'Communication and collaboration'), ('2', 'Automation and integration'), ('3', 'Security and risk management'), ('4', 'Intelligence and analytics')], max_length=256), blank=True, default=list, null=True, size=None, verbose_name='IT System capabilities'),
        ),
        migrations.AddField(
            model_name='itsystem',
            name='critical_period',
            field=models.CharField(blank=True, help_text='Is there a period/season when this system is most important?', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='itsystem',
            name='function',
            field=registers.models.ChoiceArrayField(base_field=models.CharField(choices=[('0', 'Planning'), ('1', 'Operation'), ('2', 'Reporting')], max_length=256), blank=True, default=list, null=True, size=None, verbose_name='IT System function(s)'),
        ),
        migrations.AddField(
            model_name='itsystem',
            name='legal_need_to_retain',
            field=models.NullBooleanField(default=None, help_text='Is there a legal or compliance need to keep the digital content in this system?'),
        ),
        migrations.AddField(
            model_name='itsystem',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='itsystem',
            name='point_of_truth',
            field=models.NullBooleanField(default=None, help_text='Is the digital content kept in this business system a single point of truth?'),
        ),
        migrations.AddField(
            model_name='itsystem',
            name='post_recovery',
            field=models.TextField(blank=True, help_text='Functional testing and post recovery procedure.', null=True, verbose_name='post recovery procedure'),
        ),
        migrations.AddField(
            model_name='itsystem',
            name='risks',
            field=registers.models.ChoiceArrayField(base_field=models.CharField(choices=[('0', 'IT System features not aligned to business processes'), ('1', 'IT System technology refresh lifecycle not safeguarded or future-proofed'), ('2', 'IT System data/information integrity and availability not aligned to business processes'), ('3', 'IT System emergency contingency and disaster recovery approach not well established'), ('4', 'IT System support arrangements not well established, value for money and/or safeguarded'), ('5', 'IT System roles and responsibilities not well established'), ('6', 'IT System solution design not aligned to department IT standards'), ('7', 'IT System change management does not consistently consider risk and security'), ('8', 'IT System incident and security management not triaged on business criticality'), ('9', 'IT System user training not well established')], max_length=256), blank=True, default=list, null=True, size=None, verbose_name='IT System risks'),
        ),
        migrations.AddField(
            model_name='itsystem',
            name='system_creation_date',
            field=models.DateField(blank=True, help_text='Date that this system went into production.', null=True),
        ),
        migrations.AddField(
            model_name='itsystem',
            name='system_health',
            field=models.PositiveIntegerField(blank=True, choices=[(0, 'Healthy'), (1, 'Issues noted'), (2, 'At risk')], null=True),
        ),
        migrations.AddField(
            model_name='itsystem',
            name='technical_recov',
            field=models.TextField(blank=True, null=True, verbose_name='technical recovery procedure'),
        ),
        migrations.AddField(
            model_name='itsystem',
            name='unique_evidence',
            field=models.NullBooleanField(default=None, help_text='Is the digital content kept in this business system unique evidence of the official business of the Department?'),
        ),
        migrations.AddField(
            model_name='itsystem',
            name='use',
            field=registers.models.ChoiceArrayField(base_field=models.CharField(choices=[('0', 'Measurement'), ('1', 'Information'), ('2', 'Wisdom'), ('3', 'Data'), ('4', 'Knowledge'), ('5', 'Intelligence')], max_length=256), blank=True, default=list, null=True, size=None, verbose_name='IT System use(s)'),
        ),
        migrations.AddField(
            model_name='itsystem',
            name='user_notification',
            field=models.TextField(blank=True, help_text='List of users/stakeholders to contact regarding incidents', null=True),
        ),
        migrations.AddField(
            model_name='itsystem',
            name='variation_iscp',
            field=models.TextField(blank=True, null=True, verbose_name='Variation to the ISCP'),
        ),
        migrations.AlterField(
            model_name='itsystem',
            name='access',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Public Internet'), (2, 'Authenticated Extranet'), (3, 'Corporate Network'), (4, 'Local System (Networked)'), (5, 'Local System (Standalone)')], default=3, help_text='The network upon which this system is accessible.'),
        ),
        migrations.AlterField(
            model_name='itsystem',
            name='authentication',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Domain/application Credentials'), (2, 'Single Sign On'), (3, 'Externally Managed')], default=1, help_text='The method by which users authenticate themselve to the system.'),
        ),
        migrations.AlterField(
            model_name='itsystem',
            name='criticality',
            field=models.PositiveIntegerField(blank=True, choices=[(1, 'Critical'), (2, 'Moderate'), (3, 'Low')], help_text='How critical is this system to P&W core functions?', null=True),
        ),
        migrations.AlterField(
            model_name='itsystem',
            name='hardwares',
            field=models.ManyToManyField(blank=True, help_text='Hardware that is used to provide this IT System', to='registers.ITSystemHardware', verbose_name='hardware'),
        ),
        migrations.AlterField(
            model_name='itsystem',
            name='softwares',
            field=models.ManyToManyField(blank=True, help_text='Software that is used to provide this IT System', to='registers.Software', verbose_name='software'),
        ),
    ]
