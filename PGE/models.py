from __future__ import unicode_literals

from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone


class Role(models.Model):
    
    WEB_FRONT_DEVELOPER = "WFD"
    BACKEND_DEVELOPER = "BD"
    ANDROID_DEVELOPER = "AD"
    iOS_DEVELOPER = "ID"
    DESIGNER = "DS"

    ROLE_CHOICES = (
        (WEB_FRONT_DEVELOPER, "WebFrontendDeveloper"),
        (BACKEND_DEVELOPER, "BackendDeveloper"),
        (ANDROID_DEVELOPER, "AndroidDeveloper"),
        (iOS_DEVELOPER, "iOSDeveloper"),
        (DESIGNER, "Designer"),
    )

    role_name = models.CharField(choices=ROLE_CHOICES, max_length=3, default=ANDROID_DEVELOPER  , unique=True)

    def __str__(self):
        return self.role_name


class Employee(models.Model):
    name = models.CharField(max_length=20, default=None)
    email = models.EmailField(max_length=30, unique=True)
    roles = models.ManyToManyField(Role)

    
    def __str__(self):
        return self.name


class Manager(models.Model):
    employee_instance = models.OneToOneField(Employee)


class Project(models.Model):
    project_name = models.CharField(max_length=100, default=None)
    start_date = models.DateField(default=datetime.now().date())
    end_date = models.DateField(default=None, null=True)
    manager = models.OneToOneField(Manager)
    employees = models.ManyToManyField(Employee)
    
    def __str__(self):
        return self.project_name


class Task(models.Model):
    task_name = models.CharField(max_length=100, default=None)
    start_date = models.DateField(default=datetime.now().date())
    deadline = models.DateField(default=datetime.now().date() + timedelta(days=30))
    employees = models.ManyToManyField(Employee)
    dimensions = models.ManyToManyField(Role)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.task_name




    
    
    



