# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-23 16:24
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=20)),
                ('email', models.EmailField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_instance', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='PGE.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(default=None, max_length=100)),
                ('start_date', models.DateField(default=datetime.date(2017, 6, 23))),
                ('end_date', models.DateField(default=None, null=True)),
                ('employees', models.ManyToManyField(to='PGE.Employee')),
                ('manager', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='PGE.Manager')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(choices=[('WFD', 'WebFrontendDeveloper'), ('BD', 'BackendDeveloper'), ('AD', 'AndroidDeveloper'), ('ID', 'iOSDeveloper'), ('DS', 'Designer')], default='AD', max_length=3, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(default=None, max_length=100)),
                ('start_date', models.DateField(default=datetime.date(2017, 6, 23))),
                ('deadline', models.DateField(default=datetime.date(2017, 7, 23))),
                ('dimensions', models.ManyToManyField(to='PGE.Role')),
                ('employees', models.ManyToManyField(to='PGE.Employee')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PGE.Project')),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='roles',
            field=models.ManyToManyField(to='PGE.Role'),
        ),
    ]