# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-23 17:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PGE', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='email',
            field=models.EmailField(max_length=30, unique=True),
        ),
    ]