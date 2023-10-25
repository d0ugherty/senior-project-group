import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'walrus.settings')
django.setup()

#from walrus.views import *
#from .models import Employee
from django.contrib.auth.models import User
from walrus.models import Employee, Task, Project
Employee.objects.all().delete()
User.objects.all().delete()
Project.objects.all().delete()
Task.objects.all().delete()

# Project 1
project = Project(project_name="Truck")
project.save()

# Task 1
task = Task()
task.task_name="clean"
task.project = project
task.save()


# User/Employee 1
user = User.objects.create_user(username="test", email="oconno65@students.rowan.edu", password="test", is_staff=True)
user.first_name = "Mark"
user.last_name = "OConnor"
user.is_superuser = True
user.save()
e = Employee(user=user)
e.save()
e.Tasks.add(task)

# User/Employee 2
user = User.objects.create_user(username="john", email="lennon@thebeatles.com", password="johnpassword", is_staff=True)
user.is_superuser = True
user.save()
e = Employee(user=user)
e.save()