from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Project(models.Model):
    project_name = models.CharField(max_length=255 )
    
"""

    date_created = models.DateTimeField()
    is_complete = models.BooleanField()
    date_completed = models.DateTimeField()
   # tasks = models.ManyToOne()
"""
class Task_Update(models.Model):
    Description = models.CharField(max_length=255)
   # Image = models.ImageField()



class Task(models.Model):
    task_name = models.CharField(max_length=255)
    task_description = models.CharField(max_length=255, blank=True)
    is_complete = models.BooleanField(default=False)
    project = models.ForeignKey(Project, null=True, on_delete=models.CASCADE)
    due_date = models.DateField(blank=True, default=date.today())
    date_created = models.DateTimeField(default=date.today)

    updates = models.ForeignKey(Task_Update, on_delete=models.CASCADE)
    date_created = models.DateTimeField()
    Date_assigned_to = models.DateTimeField() # when the employee is supposed to start working on it
    due_date = models.DateTimeField()
    date_completed = models.DateTimeField()
    Project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    Assigned_emp = models.ManyToManyRel(User)
    Time_spent_min = None
    Time_spent_hour = None
    if is_complete == True:
        tot_sec = date_completed.total_seconds() - date_created.total_seconds()
        Time_spent_min = tot_sec / 60
        Time_spent_hour = Time_spent_min / 6


class Employee(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    Tasks = models.ManyToManyField(Task, blank=True)
    employee_id = models.IntegerField()

    dept = models.CharField(max_length=255)
    #Shifts = models.OneToManyField(Shift)
    isManager = models.BooleanField()
    #Days_request_off = models.OneToManyField(Request_off)
    #Availability = OneToMany(avilable_time)
