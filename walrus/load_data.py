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
task.task_description="At the entrance of the store, prepare the new seasonal display."
task.project = project
task.save()

# Task 2
task2 = Task()
task2.task_name="unload Truck"
task2.save()

# User/Employee 1
user = User.objects.create_user(username="test", email="oconno65@students.rowan.edu", password="test", is_staff=True)
user.first_name = "John"
user.last_name = "Smith"
user.is_superuser = True
user.save()
e = Employee(user=user)
e.save()
e.Tasks.add(task)
e.Tasks.add(task2)

# User/Employee 2
user = User.objects.create_user(username="john", email="lennon@thebeatles.com", password="johnpassword", is_staff=True)
user.is_superuser = True
user.save()
e = Employee(user=user)
e.save()