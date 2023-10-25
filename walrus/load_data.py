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










user = User.objects.create_user(username="test", email="oconno65@students.rowan.edu", password="test", is_staff=True)
user.first_name = "Mark"
user.last_name = "OConnor"
user.is_superuser = True
user.save()
e = Employee(user=user)
e.save()


user = User.objects.create_user(username="john", email="lennon@thebeatles.com", password="johnpassword", is_staff=True)
user.is_superuser = True
user.save()
e = Employee(user=user)
e.save()