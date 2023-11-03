from django import forms

from .models import *
TIME_CHOICES = (
('Not available', 'Not available'),
('7:00am', '7:00am'),
('8:00am', '8:00am'),
('9:00am', '9:00am'),
('10:00am', '10:00am'),
('11:00am', '11:00am'),
('12:00pm', '12:00pm'),
('1:00pm', '1:00pm'),
('2:00pm', '2:00pm'),
('3:00pm', '3:00pm'),
('4:00pm', '4:00pm'),
('5:00pm', '5:00pm'),
('6:00pm', '6:00pm'),
('7:00pm', '7:00pm'),
('8:00pm', '8:00pm'),
('9:00pm', '9:00pm'),
('19:00pm', '10:00pm'),

)
class availabilityForm(forms.Form):
    sunday_start = forms.ChoiceField(choices=TIME_CHOICES)
    sunday_end = forms.ChoiceField(choices=TIME_CHOICES)
    monday_start = forms.ChoiceField(choices=TIME_CHOICES)
    monday_end = forms.ChoiceField(choices=TIME_CHOICES)
    tuesday_start = forms.ChoiceField(choices=TIME_CHOICES)
    tuesday_end = forms.ChoiceField(choices=TIME_CHOICES)
    wednesday_start = forms.ChoiceField(choices=TIME_CHOICES)
    wednesday_end = forms.ChoiceField(choices=TIME_CHOICES)
    thursday_start = forms.ChoiceField(choices=TIME_CHOICES)
    thursday_end = forms.ChoiceField(choices=TIME_CHOICES)
    friday_start = forms.ChoiceField(choices=TIME_CHOICES)
    friday_end = forms.ChoiceField(choices=TIME_CHOICES)
    saturday_start = forms.ChoiceField(choices=TIME_CHOICES)
    saturday_end = forms.ChoiceField(choices=TIME_CHOICES)



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

class employeeIdSearch(forms.Form):
    employee_id = forms.CharField(label="Employee ID Number",max_length=100, required=False)


class updateTask(forms.Form):
    description = forms.CharField(max_length=250)
    image = forms.ImageField(label="image",required=False)
