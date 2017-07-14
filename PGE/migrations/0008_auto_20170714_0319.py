# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-14 03:19
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PGE', '0007_auto_20170712_1134'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='dimensions',
        ),
        migrations.AlterField(
            model_name='project',
            name='start_date',
            field=models.DateField(default=datetime.date(2017, 7, 14)),
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.DateField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='employees',
            field=models.ManyToManyField(to='PGE.Selection'),
        ),
        migrations.AlterField(
            model_name='task',
            name='start_date',
            field=models.DateField(default=datetime.date(2017, 7, 14)),
        ),
    ]