
from __future__ import unicode_literals

from django.contrib.auth.models import User
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

    role_name = models.CharField(choices=ROLE_CHOICES, max_length=3, default=ANDROID_DEVELOPER, unique=True)
    
    def __str__(self):
        return self.role_name


class Priority(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    magnitude = models.IntegerField()


class Employee(models.Model):
    user = models.OneToOneField(User, default=None)
    priority = models.ManyToManyField(Priority)

    
    def __str__(self):
        return self.name


class Manager(models.Model):
    employee_instance = models.OneToOneField(Employee)


class Selection(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    employees = models.ManyToManyField(Employee)


class Project(models.Model):
    project_name = models.CharField(max_length=100, default=None)
    start_date = models.DateField(default=datetime.now().date())
    end_date = models.DateField(default=None, null=True)
    manager = models.ForeignKey(Manager)
    employees = models.ManyToManyField(Employee)
    selections = models.ManyToManyField(Selection)  
    
    def __str__(self):
        return self.project_name


class Task(models.Model):
    task_name = models.CharField(max_length=100, default=None)
    start_date = models.DateField(default=datetime.now().date())
    deadline = models.DateField(default=None, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    employees = models.ManyToManyField(Selection)
    is_complete = models.BooleanField(default=False)


class STask(models.Model):
    task_name = models.CharField(max_length=100, default=None)
    is_complete = models.BooleanField(default=False)    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
        
    def __str__(self):
        return self.task_name


class Session(models.Model):

    WORK_FROM_HOME = "WFH"
    WORK_FROM_OFFICE = "WFO"
    
    
    WORK_CHOICES = (
        (WORK_FROM_HOME, "Work from home"),
        (WORK_FROM_OFFICE, "Work from Office"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date_time = models.DateTimeField(auto_now=True)
    end_date_time = models.DateTimeField(auto_now=True)
    work_type = models.CharField(max_length=3, choices=WORK_CHOICES, default=WORK_FROM_OFFICE)

    def __str__(self):
        return self.user.email

    
class Absence(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField(default=None)
    end_date = models.DateField(default=None)


    def __str__(self):
        return self.user.email







    
    
    



