from django import forms

from .models import *


STATUS_CHOICES = (
('n/a', 'n/a'),
('incomplete', 'incomplete'),
('complete', 'complete'),)

class taskSearchForm(forms.Form):
    task_name = forms.CharField(label="Task name", max_length=100, required=False)
    project_name = forms.CharField(label="Project name", max_length=100, required=False)
    
    #Change Due_date to be a calander selection at some point
    due_date = forms.CharField(label="Due Date", max_length=100, required=False)
    status = forms.ChoiceField(choices=STATUS_CHOICES)