from django.contrib import admin
from walrus.models import Employee
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from .models import *

# Register your models here
admin.site.register(Project)
admin.site.register(Task)

class EmployeeInLine(admin.StackedInline):
    model = Employee
    can_delete = False #can't delete an Employee without deleting the corresponding User
    verbose_name_plural = 'Employee'

class CustomizedUserAdmin(UserAdmin):
    inlines = (EmployeeInLine, )

admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)
admin.site.register(Employee)