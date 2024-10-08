from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import date, datetime, timedelta

class Project(models.Model):
    project_name = models.CharField(max_length=255 )
    due_date = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.project_name
    

class Task(models.Model):
    task_name = models.CharField(max_length=255)
    task_description = models.CharField(max_length=255, blank=True)
    is_complete = models.BooleanField(default=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)

    date_created = models.DateTimeField(blank=True, auto_now_add=True)
    date_assigned_to = models.DateTimeField(blank=True, null=True) # when the employee is supposed to start working on it
    due_date = models.DateField(blank=True, null=True)
    date_completed = models.DateTimeField(blank=True, null=True)
    wont_complete = models.BooleanField(default=False, null=True)
   

class Task_Update(models.Model):
    description = models.CharField(max_length=255, blank=True)
    #image
    task = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True)
    venue_image = models.ImageField(null=True, blank=True, upload_to="images/")

 
    
class Shift(models.Model):
     date = models.DateField(null=True)
     start = models.CharField(max_length=255, blank=True, null=True)  
     end = models.CharField(max_length=255, blank=True, null=True)  
     to_be_taken = models.BooleanField(default=False) 
     clocked_in = models.BooleanField(default=False)
     def day_of_week(self):
        return self.date.weekday()
         
class Availability(models.Model):
    sunday_start = models.CharField(max_length=255, blank=True, null=True)
    sunday_end = models.CharField(max_length=255, blank=True, null=True)
    monday_start = models.CharField(max_length=255, blank=True, null=True)
    monday_end = models.CharField(max_length=255, blank=True, null=True)
    tuesday_start = models.CharField(max_length=255, blank=True, null=True)
    tuesday_end = models.CharField(max_length=255, blank=True, null=True)
    wednesday_start = models.CharField(max_length=255, blank=True, null=True)
    wednesday_end = models.CharField(max_length=255, blank=True, null=True)
    thursday_start = models.CharField(max_length=255, blank=True, null=True)
    thursday_end = models.CharField(max_length=255, blank=True, null=True)
    friday_start = models.CharField(max_length=255, blank=True, null=True)
    friday_end = models.CharField(max_length=255, blank=True, null=True)
    saturday_start = models.CharField(max_length=255, blank=True, null=True)
    saturday_end = models.CharField(max_length=255, blank=True, null=True)

class Role(models.Model):
    name = models.CharField(max_length=255,unique=True)
    description = models.TextField()
    def __str__(self):
            return self.name
    
class Request_Off(models.Model):
    description = models.CharField(max_length=255, blank=True)
    start = models.CharField(max_length=255, blank=True, null=True)  
    end = models.CharField(max_length=255, blank=True, null=True)


class Notification (models.Model):
     message = models.TextField()
     created_at = models.DateTimeField(auto_now_add=True)
     marked_as_read = models.BooleanField(default=False)
     def __str__(self):
          return self.message

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    Tasks = models.ManyToManyField(Task, blank=True)
    is_manager = models.CharField(
        max_length=6,
        default='No',
        choices=[('Yes', 'Yes'),('No', 'No')]
    )

    def __str__(self):
        name = self.user.first_name + " " + self.user.last_name
        return name

    employee_id = models.IntegerField(null=True, blank=True)
    dept = models.CharField(max_length=255, blank=True, null=True) ## this could possibly be model
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True)
    Shifts = models.ManyToManyField(Shift, null=True, blank=True)
    availability = models.OneToOneField(Availability, on_delete=models.CASCADE, null=True, blank=True)

    profile_pic = models.ImageField(null=True, blank=True, upload_to="images/")
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    Request_Offs = models.ManyToManyField(Request_Off, null=True, blank=True)

    notifications = models.ManyToManyField(Notification, blank=True)

class Time_Spent(models.Model):
        task = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True)
        employee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True)
        in_progress = models.BooleanField(default=False, null=True)
        total_time = models.DurationField(default=timedelta, blank=True)
        last_clock_in = models.DateTimeField(null=True)


     
     
