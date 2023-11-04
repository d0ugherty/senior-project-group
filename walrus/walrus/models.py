from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta

class Project(models.Model):
    project_name = models.CharField(max_length=255 )
    
"""

    date_created = models.DateTimeField()
    is_complete = models.BooleanField()
    date_completed = models.DateTimeField()
   # tasks = models.ManyToOne()
"""

   # Image = models.ImageField()



class Task(models.Model):
    task_name = models.CharField(max_length=255)
    task_description = models.CharField(max_length=255, blank=True)
    is_complete = models.BooleanField(default=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, default=date.today())
    Date_assigned_to = models.DateTimeField(blank=True, null=True) # when the employee is supposed to start working on it
    due_date = models.DateTimeField(blank=True, null=True)
    date_completed = models.DateTimeField(blank=True, null=True)

    

class Task_Update(models.Model):
    description = models.CharField(max_length=255, blank=True)
    #image
    task = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True)
    venue_image = models.ImageField(null=True, blank=True, upload_to="images/")


    
    #Project_id = models.ForeignKey(Project, on_delete=models.CASCADE)

class Shift(models.Model):
     date = models.DateField(null=True)
     start = models.CharField(max_length=255, blank=True, null=True)  
     end = models.CharField(max_length=255, blank=True, null=True)  
     to_be_taken = models.BooleanField(default=False)

class Employee(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    Tasks = models.ManyToManyField(Task, blank=True)
    is_manager = models.CharField(
        max_length=6,
        default='No',
        choices=[('Yes', 'Yes'),('No', 'No')]
    )

    def __str__(self):
        return self.user.username

    employee_id = models.IntegerField(null=True, blank=True)

    dept = models.CharField(max_length=255, blank=True, null=True)
    Shifts = models.ManyToManyField(Shift, null=True, blank=True)
    #Days_request_off = models.OneToManyField(Request_off)
    #Availability = OneToMany(avilable_time)



class Time_Spent(models.Model):
        task = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True)
        employee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True)
        in_progress = models.BooleanField(default=False, null=True)
        total_time = models.DurationField(default=timedelta, blank=True)
        last_clock_in = models.DateTimeField(null=True)
