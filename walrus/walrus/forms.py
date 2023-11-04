from django import forms

from .models import *


class DateInput(forms.DateInput):
    input_type = 'date'

STATUS_CHOICES = (
('n/a', 'n/a'),
('incomplete', 'incomplete'),
('complete', 'complete'),
('In Progress', 'In Progress'))

class taskSearchForm(forms.Form):
    task_name = forms.CharField(label="Task name", max_length=100, required=False)
    project_name = forms.CharField(label="Project name", max_length=100, required=False)
    
    date = forms.DateField(label="Due Date", widget=DateInput, required=False)
    #Change Due_date to be a calander selection at some point
    status = forms.ChoiceField(choices=STATUS_CHOICES)

class addTask(forms.Form):
    task_name = forms.CharField(max_length=100)
    description = forms.CharField(max_length=250)

"""
    Employee ID Input Field

    Used for getting employee stats
"""
class employeeIdSearch(forms.Form):
    employee_id = forms.CharField(label="Enter Employee ID Number",max_length=100, required=False)


class updateTask(forms.Form):
    description = forms.CharField(max_length=250)
    image = forms.ImageField(label="image",required=False)
