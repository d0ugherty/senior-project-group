import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'walrus.settings')
django.setup()

#from walrus.views import *
#from .models import Employee
from django.contrib.auth.models import User
from walrus.models import Employee, Task, Project, Task_Update, Time_Spent
Time_Spent.objects.all().delete()
Task_Update.objects.all().delete()
Employee.objects.all().delete()
User.objects.all().delete()
Project.objects.all().delete()
Task.objects.all().delete()


# Project 1
project = Project(project_name="Truck")
project.save()

# Task 1
task = Task()
task.task_name="set up entrance display"
task.project = project
task.save()

# Task 2
task2 = Task()
task2.task_name="unload Truck"
task2.save()


"""
    These tasks can be part of the same Project

"""

# Task 3
# This task is complete 
task3 = Task()
task3.task_name = "Setup Christmas light display"
task3.is_complete = True
task3.date_created = '2023-10-24 11:25:20'
task3.Date_assigned_to = '2023-10-25 09:30:59'
task3.due_date = '2023-10-26 23:59:59'
task3.date_completed = '2023-10-25 14:13:27'
task3.save()

# Task 4
# This task is in progress
task4 = Task()
task4.task_name = "Setup reindeer display"
task4.date_created = '2023-10-24 11:25:20'
task4.Date_assigned_to = '2023-10-25 09:30:59'
task4.due_date = '2023-10-26 23:59:59'
task4.date_completed = None
task4.is_complete = False
task4.save()

#Task 5
task5 = Task()
task5.task_name = "Setup Santa Clause display"
task5.date_created = '2023-10-24 11:25:20'
task5.Date_assigned_to = '2023-10-25 09:30:59'
task5.due_date = '2023-10-26 23:59:59'
task5.date_completed = None
task5.is_complete = False
task5.save()


# User/Employee 1
user = User.objects.create_user(username="test", 
                                email="oconno65@students.rowan.edu", 
                                password="test", 
                                is_staff=True)
user.first_name = "John"
user.last_name = "Smith"
user.is_superuser = True
user.save()
e = Employee(user=user, employee_id = 1)
e.save()
e.Tasks.add(task)
e.Tasks.add(task2)

# User/Employee 2
user = User.objects.create_user(username="john", 
                                email="lennon@thebeatles.com", 
                                password="johnpassword", 
                                is_staff=True)
user.is_superuser = True
user.save()
e = Employee(user=user, employee_id = 2)
e.save()

# User/Employee 3

user = User.objects.create_user(username="walker", 
                                email="doughe38@students.rowan.edu", 
                                password = "password",
                                is_staff=True)
user.first_name = "Walker"
user.last_name = "Texas Ranger"
user.is_superuser = True
user.save()
e = Employee(user=user, employee_id = 3)
e.save()
e.Tasks.add(task3)
e.Tasks.add(task4)
e.Tasks.add(task5)
