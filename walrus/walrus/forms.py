from django import forms

from .models import *


class DateInput(forms.DateInput):
    input_type = 'date'

STATUS_CHOICES = (
('n/a', 'n/a'),
('incomplete', 'incomplete'),
('complete', 'complete'),)

class taskSearchForm(forms.Form):
    task_name = forms.CharField(label="Task name", max_length=100, required=False)
    project_name = forms.CharField(label="Project name", max_length=100, required=False)
    
    date = forms.DateField(label="Due Date", widget=DateInput, required=False)
    #Change Due_date to be a calander selection at some point
    status = forms.ChoiceField(choices=STATUS_CHOICES)

class addTask(forms.Form):
    task_name = forms.CharField(max_length=100)
    description = forms.CharField(max_length=250)
    project = forms.ModelChoiceField(queryset=Project.objects.all(),required=False)
    employee = forms.ModelChoiceField(queryset=Employee.objects.all(),required=False)

    
class employeeIdSearch(forms.Form):
    employee_id = forms.CharField(label="Employee ID Number",max_length=100, required=False)


class updateTask(forms.Form):
    description = forms.CharField(max_length=250)
    image = forms.ImageField(label="image",required=False)


class projectForm(forms.Form):
    name = forms.CharField(label="Project Name",max_length=250)
    due_date = forms.DateField(label="Due Date (optional)", widget=DateInput, required=False)