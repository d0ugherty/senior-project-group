import os
import django
import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'walrus.settings')
django.setup()

#from walrus.views import *
#from .models import Employee
from django.contrib.auth.models import User
from walrus.models import Employee, Task, Project, Task_Update, Time_Spent, Availability, Shift
Availability.objects.all().delete()
Time_Spent.objects.all().delete()
Task_Update.objects.all().delete()
Employee.objects.all().delete()
User.objects.all().delete()
Project.objects.all().delete()
Task.objects.all().delete()
Shift.objects.all().delete()
# Update 1
update_1 = Task_Update(description="Task has been started")
update_1.save()
# Update 2
update_2 = Task_Update(description="Task is 50 percent done")
update_2.save()
# Project 1
project = Project(project_name="Truck")
project.save()

# Task 1
task = Task()
task.task_name="set up entrance display"
task.task_description="At the entrance of the store, prepare the new seasonal display."
task.project = project
task.date_assigned_to = '2023-10-25 09:30:59'
task.save()

task.task_update_set.add(update_1)
task.task_update_set.add(update_2)

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
task3.date_assigned_to = '2023-10-25 09:30:59'
task3.due_date = '2023-10-26 23:59:59'
task3.date_completed = '2023-10-25 14:13:27'
task3.save()

# Task 4
# This task is in progress
task4 = Task()
task4.task_name = "Setup reindeer display"
task4.date_created = '2023-10-24 11:25:20'
task4.date_assigned_to = '2023-10-25 09:30:59'
task4.due_date = '2023-10-26 23:59:59'
task4.date_completed = None
task4.is_complete = False
task4.save()

#Task 5
task5 = Task()
task5.task_name = "Setup Santa Clause display"
task5.date_created = '2023-10-24 11:25:20'
task5.date_assigned_to = '2023-10-25 09:30:59'
task5.due_date = '2023-10-26 23:59:59'
task5.date_completed = None
task5.is_complete = False
task5.to_be_taken= True
task5.save()

# shift 1

shift_1 = Shift(date=datetime.datetime.today(), start="7:00am", end="12:00pm")
shift_1.to_be_taken=True
shift_1.save()

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
e.Shifts.add(shift_1)
# avil
availability = Availability(sunday_start='Not available', sunday_end = 'Not available', monday_start = '7:00am', monday_end = '12:00pm')
availability.save()
e.availability =  availability
print(e.availability)
e.save()
# User/Employee 2
user = User.objects.create_user(username="john", 
                                email="lennon@thebeatles.com", 
                                password="johnpassword", 
                                is_staff=True)
user.is_superuser = True
user.first_name = "Matt"
user.last_name = "Smith"
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
