import calendar
from django import forms
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db import transaction
from django.views import generic
from django.utils.safestring import mark_safe
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
import datetime
from datetime import datetime, timedelta
from calendar import month_name
from calendar import HTMLCalendar

from .models import Task, Shift
from .forms import *
from .util import *
from .multiforms import MultiFormView
from datetime import datetime,timezone

from django.contrib import messages

import re



def availability(request, employee_id):

    employee = Employee.objects.get(pk=employee_id)

    # If employee updates availability
    if request.method == "POST":
        
        if employee.availability == None:
                availability = Availability()
                availability.save()
                employee.availability = availability
                employee.save()
        
        # Sets availability
        set_availability(request, employee)
        # returning to home page
        today = datetime.today()
        return HttpResponseRedirect('/home/' + str(employee_id) + '/' + str(today.day) + '/' + str(today.month) + '/' + str(today.year))

    #   If the employee already has availability set this will load the page with the correct availability
    if employee.availability != None:
        dict = {
            'sunday_start' : employee.availability.sunday_start, 'sunday_end' : employee.availability.sunday_end,
            'monday_start' : employee.availability.monday_start, 'monday_end' : employee.availability.monday_end,
            'tuesday_start' : employee.availability.tuesday_start, 'tuesday_end' : employee.availability.tuesday_end,
            'wednesday_start' : employee.availability.wednesday_start, 'wednesday_end' : employee.availability.wednesday_end,
            'thursday_start' : employee.availability.thursday_start, 'thursday_end' : employee.availability.thursday_end,
            'friday_start' : employee.availability.friday_start, 'friday_end' : employee.availability.friday_end,
            'saturday_start' : employee.availability.saturday_start, 'saturday_end' : employee.availability.saturday_end,
             }
    else:
        dict = {}

    form = availabilityForm(initial=dict)

    return render(request, 'availability.html', {'form':form})

def request_time_off(request, employee_id):
    user = request.user
   
   # if user submits a request off form
    if request.method == 'POST':
        
        form = requestOffForm(request.POST)
        if form.is_valid():
            
                description = form.cleaned_data['description']
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']
                print(start_date)
                new_request_off = Request_Off(description=description, start=start_date, end=end_date)
                new_request_off.save()
                user.employee.Request_Offs.add(new_request_off)
    form = requestOffForm()

    return render(request, 'request_time_off.html', {'form':form})

def profile(request, employee_id):
    user = request.user

   # hello = "123"
   # return render(request,'htmx_fragments/noti.html', {'hello':hello})
    return render (request, 'new_profile.html',{'user':user})

def edit_profile(request, employee_id):
    user = request.user
    if request.method == 'POST':
        form = change_profile_image_Form(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data.get('profile_pic')
            if image != None:
                user.employee.profile_pic = image
                user.employee.save()

        # Reading from form
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        # PUT PHONE NUMBER AND IMAGE

        # Assigning new attributes to user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.employee.phone_number = phone_number
        user.employee.save()
        user.save()

        return render (request, 'new_profile.html',{'user':user})
    
    pic_form = change_profile_image_Form()
    return render (request, 'edit_profile.html',{'user':user, 'form':pic_form})
# after user logs in this redirects them to home page
def home_redirect(request):
    user=request.user
    if user.is_authenticated:
     
     today = datetime.today()
     url = 'home/' + str(user.employee.pk) + '/' + str(today.day) + '/' + str(today.month) + '/' + str(today.year)
       
     return redirect(url)
    else:
        return HttpResponseRedirect('/accounts/login/')
    
    return render(request, 'home.html')

def python_test(request):
    user = datetime.ass
    
def list_tasks(request):
    try:
        tasks = Task.objects.all()
    except: 
        raise Http404('No Tasks Found')


    if request.method == "POST":

        if "search" in request.POST:
            task_name = request.POST.get('task_name')
            project_name = request.POST.get('project_name')
            status = request.POST.get('status')
            due_date = request.POST.get('date')
            #print(due_date)
            # Getting the list of tasks that 
            tasks = find_tasks(task_name, project_name, due_date, status)
        #if (tasks == None) :
            #print(tasks[0].due_date)
        if "delete" in request.POST:

            task_pk = request.POST.get('delete')
            task = Task.objects.get(pk=task_pk)
            print(task)
            task.delete()

    form = taskSearchForm()
        
    return render(request, 'task_list.html', {
        'tasks': tasks, 'form':form, 
    })

def create_project(request):
    user = request.user
    if user.employee.is_manager == 'No':
         return render(request, 'notAManager.html')

    success_message = False
    if request.method == 'POST':
        name = request.POST.get('name')
        date = request.POST.get('due_date')
        print(date)
        if date == "":
            project = Project(project_name=name)
        else:
            project = Project(project_name=name,due_date=date)        
        project.save()
        success_message = True


    form = projectForm()
    return render(request, 'create_project.html', {'form':form,'success_message':success_message})


def task_detail (request, task_id):
    form = taskSearchForm()

    task = Task.objects.get(id=task_id)
    employees = task.employee_set.all()
    updates = task.task_update_set.all()

    return render (request, 'task_detail.html', {
        'task': task,
        'form' : form,
        'updates' : updates,
        'employees':employees
    })

def home_page(request, employee_id, day, month, year):
    
    screen_date = date(year,month,day)
    employee = Employee.objects.get(pk=employee_id)
    shift = employee.Shifts.filter(date=screen_date)
    if shift.first() != None:
        shift = shift.first()
    
    # should filter all tasks that have not been completed
    # date from url
    tasks =  employee.Tasks.filter(is_complete=False, date_assigned_to__range=( date.min, screen_date), wont_complete = False).order_by('due_date') | employee.Tasks.filter(is_complete=False, date_assigned_to=None, wont_complete = False).order_by('due_date')
    
    if request.method == 'POST':
        # go through the tasks and find the object that was selected and clock in or out
        # I just have the buttons named as the task object they are associated with       
        for x in tasks:
            # print(str(x) + " complete")            
            # each button is labeled with either clock or complete so we know what to do
            if str(x) + " clock" in request.POST:
                print(str(employee_id))
                #Getting the Time_spent object associated with the task and employee
                if (Time_Spent.objects.filter(employee=employee_id,task=x.pk)):
                    time_record = Time_Spent.objects.get(employee=employee_id,task=x.pk)
                   
                    adjust_clock_in(time_record)
                #if we need to create a new time object
                else:
                    time_record = Time_Spent(employee=employee, task=x)
                    time_record.save()
                    adjust_clock_in(time_record)
            
            # if the task was selected as completed
            elif str(x) + " complete" in request.POST:
                print(str(x) + " complete")
                x.is_complete = True
                x.save()
                tasks =  employee.Tasks.filter(is_complete=False, date_assigned_to__range=( date.min, screen_date), wont_complete = False).order_by('due_date') | employee.Tasks.filter(is_complete=False, date_assigned_to=None, wont_complete = False).order_by('due_date')
                context = {'tasks':tasks,'employee_id':employee_id,
                                             'day':day, 'month':month, 'year':year}
                return render(request, 'htmx_fragments/home_page_tasks.html', context)
        if "to_be_taken" in request.POST:
            shift_pk = request.POST['to_be_taken']
            shift = Shift.objects.get(pk=shift_pk)
             
            if shift.to_be_taken == False:
                 shift.to_be_taken = True
            else:
                shift.to_be_taken = False
            print(shift.to_be_taken)
            shift.save()   
            return redirect('home')
        if "shift_clock_in" in request.POST:
            shift_pk = request.POST['shift_clock_in']
            shift = Shift.objects.get(pk=shift_pk)
            shift.clocked_in = True
            shift.save()
            return redirect('home')
    return render(request, 'home_page.html',{ 'employee':employee, 'tasks':tasks, 'shift':shift, 'employee_id':employee_id,
                                             'day':day, 'month':month, 'year':year})


def home_page_tasks(request, employee_id, day, month, year):
    screen_date = date(year,month,day)
    employee = Employee.objects.get(pk=employee_id)
    
    # should filter all tasks that have not been completed
    # date from url
    tasks =  employee.Tasks.filter(is_complete=False, date_assigned_to__range=( date.min, screen_date), wont_complete = False).order_by('due_date') | employee.Tasks.filter(is_complete=False, date_assigned_to=None, wont_complete = False).order_by('due_date')
    context = {'tasks':tasks,'employee_id':employee_id,
                                             'day':day, 'month':month, 'year':year}
    return render(request, 'htmx_fragments/home_page_tasks.html', context)

class CalendarView(generic.ListView):
    model = Task
    template_name = 'calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
      

        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

"""
    Loads the manager tools page
    TO DO: Check for user type
"""
def load_manager_tools(request):
    user = request.user
    if user.employee.is_manager == 'No':
         return render(request, 'notAManager.html')



    return render(request, 'manager_tools.html')

"""
    Retrieves the 'destination' name of a button
    on the Manager Home page and 
    Redirects the user to the appropriate page 
    according to the 'destionation' string

    Currently, the un-implemented pages will default to "invalid destination"

    TO DO: Add more redirects as project progresses
"""
def manager_tools_redirect(request):
    destination = request.POST.get('destination')
    match destination:
        case "/add_task/":
            return HttpResponseRedirect(destination)
        case "/list_tasks/":
            return HttpResponseRedirect(destination)
        case "/employee_stats/":
            return HttpResponseRedirect(destination)
        case "/create_project/":
            return HttpResponseRedirect(destination)
        case "/schedule_employee/":
            return HttpResponseRedirect(destination)
        case "/manage_roles/":
            return HttpResponseRedirect(destination)
        case _:
            return HttpResponse("Invalid destination", status=400)

"""
    View for the loading employee stats page

    search_input is a CharField form and employee_id is an integer type
    in the database.
    
    validate_id checks if the input is a digit and if so 
    casts the input as an integer

"""

def employee_stats(request):
    user = request.user
    if user.employee.is_manager == 'No':
         return render(request, 'notAManager.html')
    
    if request.method == 'POST':
        
        form = employeeIdSearch(request.POST)
        
        if form.is_valid():

            employee = form.cleaned_data['employee'] 
            status = form.cleaned_data['status']
            print(status)
            if employee != None:
            # get tasks
                if status == 'n/a':
                    tasks = employee.Tasks.all()
                else:
                    if status == "complete":
                        status = True
                        wont_complete = False
                    elif status == "incomplete":
                        status = False
                        wont_complete = False
                    elif status=='failed':
                        status = False
                        wont_complete = True
                    tasks = employee.Tasks.filter(is_complete=status, wont_complete=wont_complete)
                name = f'{employee.user.first_name} {employee.user.last_name}' 

                # looping through all of the time_spent objects associated with the tasks
                time_spent = []
                for t in tasks:
                    if (Time_Spent.objects.filter(employee=employee.pk,task=t.pk)):
                       time_record = Time_Spent.objects.get(employee=employee.pk,task=t.pk)
                       time_spent.append(time_record.total_time)
                    else:
                       time_spent.append(None)

                return render(request, 'employee_stats.html', {'form': form, 
                                                            'tasks': tasks, 
                                                            'employee': employee,
                                                            'employee_name': name,
                                                            'time_spent' : time_spent})
    else:
        form = employeeIdSearch()
    return render(request, 'employee_stats.html', {'form' : form })

"""
    Create and manage employee positions
    TO DO:    
    > Remove roles and positions

"""


def manage_roles(request):
    context = {}
    if request.method == 'POST':
        # Role creation/deletion
        if "submit_role" in request.POST:
            handle_role_submission(request, context)
       # Employee assignment 
        if "assign_role" in request.POST:
            handle_role_assignment(request, context)
        # Role removal
        if "delete_role" in request.POST:
            handle_role_removal(request, context)

    if 'msg' in request.session:
        context['msg'] = request.session.pop('msg')
    return blank_role_form(request, 'manage_roles.html', context)

"""
    Helper functions to reduce code duplication
    and make the manage_roles view more readable

"""
def blank_role_form(request, template, context):  
    context['create_role_form'] = CreateRoleForm()
    context['assign_role_form'] = AssignRoleForm()
    context['delete_role_form'] = DeleteRoleForm()
    return render(request, template, context)

"""
    Handles the creation of new role and position entries
    into the database. 

    Validity is checked by by getting names of
    existing roles. The Role model has a one to many relationship with 
    Employee so only one of each name is required for each position in the store.
"""

def handle_role_submission(request, context):
    create_role_form = CreateRoleForm(request.POST)
    context['create_role_form'] = create_role_form

    if create_role_form.is_valid():
        role_name = create_role_form.cleaned_data['role_name'].strip()
        role_desc = create_role_form.cleaned_data['description'].strip()

        if not Role.objects.filter(name=role_name).exists():
            create_role(request, context, role_name, role_desc)
            return redirect('manage_roles')
    
        else:
            context['msg'] = f'Role submission unsuccessful: Role {role_name} already exists'
            return blank_role_form(request, 'manage_roles.html', context)
    return blank_role_form(request, 'manage_roles.html', context)

"""
    Creates the role record in the database 
"""
def create_role(request,context,name,desc):
    try:
        new_role = Role.objects.create(name=name, description=desc).validate_unique()
        context['role'] = new_role
        request.session['msg'] = f'Role {name} successfully created'
    except ValidationError as error:
        request.session['msg'] = f'Role submission unsuccessful: {error}'

"""
    Handles the assignment of roles and positions to employees
"""

def handle_role_assignment(request,context):
    assign_role_form = AssignRoleForm(request.POST)
    context['assign_role_form'] = assign_role_form
    
    if assign_role_form.is_valid():
        role = assign_role_form.cleaned_data['roles']
        employee = assign_role_form.cleaned_data['assign_employee']
            
        msg = get_assign_msg(employee, role)

        employee.role = role
        employee.save()
        request.session['msg'] = msg
        return redirect('manage_roles')
    else:
        return blank_role_form(request, 'manage_roles.html', context)

def get_assign_msg(employee, role):
    if employee.role_id == role.id:
        return  f'Employee {employee} is already assigned to {role}!'
    else:
        return f'Employee {employee} has been assigned to {role}'

"""
    Handles the removal of positions and roles from the database

"""
def handle_role_removal(request, context):
    delete_role_form = DeleteRoleForm(request.POST)
    context['delete_role_form'] = delete_role_form

    if delete_role_form.is_valid():
        role = delete_role_form.cleaned_data['role']
         
        # If employees are found to be assigned to the position,
        # the user is alerted to remove those assignments before deleting
        if check_employees(request, role, context):
            context['msg'] = f'Please unassign employees from {role}' 
            return blank_role_form(request, 'manage_roles.html', context)

        else:
            print("deleting role") 
            role.delete()
            print("role deleted")
            request.session['msg'] = "position deleted"
            return redirect('manage_roles')
    else:
        print(delete_role_form.errors)
        return blank_role_form(request, 'manage_roles.html', context)

def check_employees(request, role, context):
    employees = []
    employees = Employee.objects.filter(role=role)
    return employees 
"""
    Add Task
"""

def add_task(request):

    user = request.user
    if user.employee.is_manager == 'No':
         return render(request, 'notAManager.html')
    success_message = False


    if request.method=='POST':
        form = addTask(request.POST)
        if form.is_valid():
            task_name = form.cleaned_data['task_name']
            task_description = form.cleaned_data['description']
            project = form.cleaned_data['project']
            employee = form.cleaned_data['employee']
            due_date = form.cleaned_data['due_date']
            assign_date = form.cleaned_data['assign_date']

            # Going to loop through each field to make sure its not empty
            # Was having issues when theses were empty
            fields ={
                    'task_name': task_name,
                    'task_description': task_description,
                    'project': project,
                    'due_date': due_date,
                    'date_assigned_to' : assign_date
            }
            nonEmptyFields = {}
            for x in fields:
                if fields[x] != "":
                    nonEmptyFields.update({x : fields[x]})
            print(nonEmptyFields)

            newTask = Task(**nonEmptyFields)
            
            newTask.save()

            success_message = True

            employee.Tasks.add(newTask)
            notification = Notification(message = "You have been assigned a new task: " + newTask.task_name)
            notification.save()
            employee.notifications.add(notification)
            #return HttpResponseRedirect('/add_task')
    
    form = addTask()
    return render(
    request, 
    'add_task.html',
    {'form': form, 'success_message':success_message}
    )


'''
Employee will need to be changed to allow for multiple employees to appear
'''


def edit_task(request, task_id):

    user = request.user
    if user.employee.is_manager == 'No':
         return render(request, 'notAManager.html')


    task = Task.objects.get(pk=task_id) 
    if request.method=='POST':
        if "edit" in request.POST:
            form = editTask(request.POST)
            if form.is_valid():
                task.task_name = form.cleaned_data['task_name']
                task.task_description = form.cleaned_data['description']
                task.project = form.cleaned_data['project']
                employee = form.cleaned_data['employee']
                task.due_date = form.cleaned_data['due_date']
                task.date_assigned_to = form.cleaned_data['assign_date']
                status = form.cleaned_data['status']
            # adjusting status
                if status == 'complete':
                    task.is_complete = True
                else:
                    task.is_complete = False
                # removing or adding employees to task
                if employee == None:
                    task.employee_set.clear()
                else:
                    employee.Tasks.add(task)

                task.save()
                notification = Notification(message = "Your task '"+task.task_name + "' has been edited")
                notification.save()
                employee.notifications.add(notification)
                # Going to loop through each field to make sure its not empty
                
            return HttpResponseRedirect('/task_detail/' + str(task_id))
        if "delete" in request.POST:
            task = Task.objects.get(pk=task_id) 
            task.delete()
            #notification = Notification(message = "Your task '"+task.task_name + "' has been deleted")
            #notification.save()
            #employee.notifications.add(notification)
            
            return redirect('home')
    # employee will need to be fixed later when we allow for multiple employees
    employees = task.employee_set.all()
    if task.is_complete == False:
        status = 'incomplete'
    else:
        status = 'complete'
    fields ={
                    'task_name': task.task_name,
                    'description': task.task_description,
                    'project': task.project,
                    'due_date': task.due_date,
                    'assign_date' : task.date_assigned_to,
                    'status' : status
                    
            }
    if employees.count() != 0:
        fields['employee'] = employees[0]

    nonEmptyFields = {}
    for x in fields:
        if fields[x] != "":
            nonEmptyFields.update({x : fields[x]})
    print(nonEmptyFields)

    #employee = task.Employee
    form = editTask(initial=nonEmptyFields)
    print(nonEmptyFields['project'])
    return render( request, 'edit_task.html', {'form':form})

def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return HttpResponseRedirect(reverse('calendar'))


def update_task_status(request,task_id):
    if request.method == "POST":
        form = updateTask(request.POST, request.FILES)
        if form.is_valid():
            description = request.POST.get('description')
            image = form.cleaned_data.get('image')
            task = Task.objects.get(pk=task_id)
            
            update = Task_Update(description=description,task=task, venue_image=image)
            update.save()
            return redirect('home')

    form = updateTask()
    return render(request, 'update_task_status.html', {'form':form})

def schedule_employee(request):
    user = request.user
    if user.employee.is_manager == 'No':
         return render(request, 'notAManager.html')
    avil = None
    employees = None
    shifts = None
    requests_off = None
    dict = {}

    if request.method == "POST":
        # Employee Avilability was searched
        
        if "search" in request.POST:
            form = employeeDropdownSearch(request.POST)
            if form.is_valid():
                employee = form.cleaned_data['employee']
                
                if employee != None:
                    avil = employee.availability
                    requests_off = employee.Request_Offs.filter(start__range=(datetime.today(), (datetime.today()+ timedelta(10000))))
                context = {'search_form':form,'avil':avil, 'requests_off':requests_off}
                return render(request, 'htmx_fragments/avil_s.html', context)


        if "save_shift" in request.POST or "select_week_form" in request.POST or "delete" in request.POST: 
            if "save_shift" in request.POST:

                employee_pk = request.POST.get('employee')
                
                date = request.POST.get('date')
                start_time = request.POST.get('start_time')
                end_time = request.POST.get('end_time')

                if employee_pk !='' and date !='' and start_time !='' and end_time !='':
                    employee = Employee.objects.get(pk=employee_pk)
                    shift = Shift(date=date, start=start_time, end=end_time)
                    
                    if (employee.Shifts.filter(date=date)):
                       old_shift = employee.Shifts.get(date=date)
                       old_shift.delete()
                    shift.save()
                    employee.Shifts.add(shift)
                else:
                    print("error missing component")
                dict = {}
            if "delete" in request.POST:
                shift_pk = request.POST.get('delete')
                shift = Shift.objects.filter(pk=shift_pk)
                shift.delete()

            if 'week_date' in request.POST:
                    date = request.POST.get('week_date')    
                    if date != '':
                        date = datetime.strptime(date, '%Y-%m-%d').date()
                        start_date, end_date = get_start_and_end(date)
        

                        
                        shiftsThisWeek = Shift.objects.filter(date__range=(start_date, end_date)).order_by('date')
                        dict = create_shift_table(shiftsThisWeek)
 
            schedule_form = scheduleEmployee()              
            select_week_form = selectWeek(initial={'week_date': date})
            context = { 'select_week_form':select_week_form,'dict':dict, 'schedule_form':schedule_form }
            return render(request, 'htmx_fragments/shift_week_schedule.html', context)
       
    search_form = employeeDropdownSearch()
    schedule_form = scheduleEmployee()
    select_week_form = selectWeek()

    return render(request, 'schedule_employee.html', 
                  {'search_form':search_form, 'avil':avil, 
                   'schedule_form':schedule_form, 'select_week_form':select_week_form,
                   'select_week_form':select_week_form, 
                    'employees':employees, 'shifts':shifts, 'dict':dict,
                    'requests_off':requests_off,
                    })

def task_failure(request, task_id):
    if request.method=='POST':
        form = failureForm(request.POST, request.FILES)
        task = Task.objects.get(id=task_id)
        if form.is_valid():
            
            if form['failure']:
                task.wont_complete = True
                description = request.POST.get('description')
                update = Task_Update(description=description,task=task)
                update.save()
        task.save()
        return redirect('home')
     
    form = failureForm()
    return render(request, 'task_failure.html',
                  { 'fail_form':form })


def shift_switch(request, employee_id):
    employee = Employee.objects.get(pk=employee_id)
    eShifts = employee.Shifts.filter()
    already_have_shift_error = False


    if request.method=='POST':
            shift_pk = request.POST['button']
            
            shift = Shift.objects.get(pk=shift_pk)
            date = shift.date
            
            # checking if employee already has a shift on that day
            if employee.Shifts.filter(date=date).exists() == False:

                shift.to_be_taken = False
                shift.employee_set.clear()
                shift.save()
                employee.Shifts.add(shift)
                already_have_shift_error = False
            else:
                already_have_shift_error = True


    all_to_be_taken_shifts = Shift.objects.filter(to_be_taken=True)
    shifts = []
    for shift in all_to_be_taken_shifts:
        if employee not in shift.employee_set.all():
            shifts.append(shift)

    # This works
    



    for e in eShifts:
        for s in shifts:
            #check for shift discrepancies
            #dont show shifts employees can't take
            if e == s:
                #shifts.exclude(s) #I will not be able to test this very well until we have a lot of data
                ""
    
    shift_employee_dict = {}
    for x in shifts:
       emp = x.employee_set.all()
       shift_employee_dict[x] = emp
    print(shift_employee_dict)
    return render(request, 'shift_switch.html', {
        'employee' : employee,
        'shifts' : shifts,
        'shift_employee_dict':shift_employee_dict,
        'already_have_shift_error':already_have_shift_error
    })

def swap_shifts(request, employee_id, shift_id):
    employee = Employee.objects.get(pk=employee_id)
    shift = Shift.objects.get(pk=shift_id)
    employees = Employee.objects.all()

    # Need to verify that the employee picking up a shift does not work that day
    date = shift.date
    print(date)
    if employee.Shifts.filter(date=date) == None:

        #find shift from existing employee and remove it
        #there HAS to be a better way to do this but I can't find anything
        
        


        for e in employees:
            for s in e.Shifts.filter():
                if (s == shift):
                    e.Shifts.get(pk=shift.pk).delete()
                    break

        #add the shift to the current employee
        #and alter the shift+save it
        shift.to_be_taken = False
        shift.save()
        employee.Shifts.add(shift)
        shifts = Shift.objects.filter(to_be_taken=True)
        return render(request, 'shift_switch.html', {
            'employee' : employee,
            'shifts' : shifts
        })

        
    else:
        shifts = Shift.objects.filter(to_be_taken=True)
        return render(request, 'shift_switch.html', {
            'employee' : employee,
            'shifts' : shifts
        })
        

def notifications(request):
    user = request.user
    employee = user.employee
    notifications = employee.notifications.all().filter(marked_as_read=False)
    #print(notifications)
    #notifications=None
    if request.method == "POST":

        key = request.POST.get("noti")
        noti = Notification.objects.get(pk=key)
        noti.marked_as_read = True
        noti.save()



    return render(request,'htmx_fragments/notifications.html', {'notifications':notifications})
        
