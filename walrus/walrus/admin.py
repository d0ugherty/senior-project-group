from django.contrib import admin
from walrus.models import Employee
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from .models import *

# import for notifcations
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import HttpResponseRedirect
from django import forms
from django.urls import path




# Register your models here
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Time_Spent)
admin.site.register(Task_Update)
admin.site.register(Availability)
admin.site.register(Shift)
admin.site.register(Request_Off)
admin.site.register(Role)

class EmployeeInLine(admin.StackedInline):
    model = Employee
    can_delete = False #can't delete an Employee without deleting the corresponding User
    verbose_name_plural = 'Employee'

class CustomizedUserAdmin(UserAdmin):
    inlines = (EmployeeInLine, )

admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)
admin.site.register(Employee)
admin.site.register(Notification)
