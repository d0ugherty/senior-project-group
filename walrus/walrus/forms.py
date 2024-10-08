from django import forms
from django.core.exceptions import ValidationError
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
('10:00pm', '10:00pm'),

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
('complete', 'complete'),
('failed','failed')
)

EDIT_TASK_STATUS = (
('incomplete', 'incomplete'),
('complete', 'complete'),

)


class taskSearchForm(forms.Form):
    task_name = forms.CharField(label="Task name", max_length=100, required=False)
    project_name = forms.CharField(label="Project name", max_length=100, required=False)
    
    date = forms.DateField(label="Due Date", widget=DateInput, required=False)
    status = forms.ChoiceField(choices=STATUS_CHOICES)

class addTask(forms.Form):
    task_name = forms.CharField(max_length=100)
    description = forms.CharField(max_length=250, required=False, widget=forms.Textarea(attrs={"rows":"4", "style":"width:100%;"}))
    project = forms.ModelChoiceField(queryset=Project.objects.all(),required=False)
    employee = forms.ModelChoiceField(queryset=Employee.objects.all())
    due_date = forms.DateField(label="Due Date", widget=DateInput, required=False)
    assign_date = forms.DateField(label="Assignment Date", widget=DateInput, required=False)
    
class editTask(forms.Form):
    task_name = forms.CharField(max_length=100)
    project = forms.ModelChoiceField(queryset=Project.objects.all(),required=False)
    description = forms.CharField(max_length=250, required=False,  widget=forms.Textarea(attrs={"rows":"4", "style":"width:100%;"}))
    employee = forms.ModelChoiceField(queryset=Employee.objects.all())
    due_date = forms.DateField(label="Due Date", widget=DateInput, required=False)
    assign_date = forms.DateField(label="Assignment Date", widget=DateInput, required=False)
    status = forms.ChoiceField(choices=EDIT_TASK_STATUS)

     
class requestOffForm(forms.Form):
    description = forms.CharField(max_length=250, required=False, widget=forms.Textarea(attrs={"rows":"4", "style":"width:100%;"}))
    start_date = forms.DateField(label="Start Date", widget=DateInput, required=False)
    end_date = forms.DateField(label="End Date", widget=DateInput, required=False)

class employeeIdSearch(forms.Form):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all(),required=True)
    status = forms.ChoiceField(choices=STATUS_CHOICES)

class employeeDropdownSearch(forms.Form):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all(),required=False)

class updateTask(forms.Form):
    description = forms.CharField(max_length=250, required=False,widget=forms.Textarea(attrs={"rows":"8", "style":"width:60%;"}))
    image = forms.ImageField(label="image",required=False)

class scheduleEmployee(forms.Form):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all(),required=False)
    date = forms.DateField(label="Date", widget=DateInput,required=False)
    start_time = forms.ChoiceField(choices=TIME_CHOICES,required=False)
    end_time = forms.ChoiceField(choices=TIME_CHOICES,required=False)


class selectWeek(forms.Form):
    week_date = forms.DateField(label="Week of", widget=DateInput, required=False)

class projectForm(forms.Form):
    name = forms.CharField(label="Project Name",max_length=250)
    due_date = forms.DateField(label="Due Date (optional)", widget=DateInput, required=False)



class CreateRoleForm(forms.Form):
    role_name = forms.CharField(label="Role/Position", max_length=50)
    description = forms.CharField(label="Description", max_length=255, required=False)

class AssignRoleForm(forms.Form):
    roles = forms.ModelChoiceField(queryset=Role.objects.all())
    assign_employee = forms.ModelChoiceField(queryset=(Employee.objects.all()),
                                            label="Assign role to an employee",
                                            required=True)
class UnassignRoleForm(forms.Form):
    unassign_employee = forms.ModelChoiceField(queryset=(Employee.objects.all()),
                                               label="Remove Employee from Current Position",
                                               required=True)
class DeleteRoleForm(forms.Form):
    role = forms.ModelChoiceField(queryset=(Role.objects.all()),
                                   label="Roles/Positions")

class failureForm(forms.Form):
    failure = forms.BooleanField(label="Task Failed")
    description = forms.CharField(max_length=250, required=False, widget=forms.Textarea(attrs={"rows":"4", "style":"width:100%;"}))
class change_profile_image_Form(forms.Form):
    profile_pic = forms.ImageField(label="image",required=False)

