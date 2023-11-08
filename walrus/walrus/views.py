import calendar
from django import forms
from django.views import generic
from django.utils.safestring import mark_safe
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.urls import reverse
import datetime
from datetime import datetime, timedelta
from calendar import month_name
from calendar import HTMLCalendar

from .models import Task
from .forms import taskSearchForm, addTask, employeeIdSearch, updateTask, editTask, projectForm
from .util import *

from datetime import datetime,timezone

from django.contrib import messages
# Imports for notifications
from walrus.admin import SendNotificationForm
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync



# after user logs in this redirects them to home page
def home_redirect(request):
    user=request.user
    if user.is_authenticated:
     today = datetime.today()
     url = 'home/' + str(user.employee.pk) + '/' + str(today.day) + '/' + str(today.month) + '/' + str(today.year)
       


     return redirect(url)
    return render(request, 'home.html')


def list_tasks(request):
    try:
        tasks = Task.objects.all()
    except: 
        raise Http404('No Tasks Found')


    if request.method == "POST":
        task_name = request.POST.get('task_name')
        project_name = request.POST.get('project_name')
        status = request.POST.get('status')
        due_date = request.POST.get('date')
       # print(due_date)
       # print(Task.objects.filter(due_date=due_date))

        
        tasks = find_tasks(task_name, project_name, due_date, status)
         #print(Task.objects.filter(project=project_object))
       # print(task_name)
       # print(project_name)
       # print(due_date)
       #print(status)
       
       # Null case 
       # if (task_name == ""):


    form = taskSearchForm()
    
    
    return render(request, 'task_list.html', {
        'tasks': tasks, 'form':form, 
    })

def create_project(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        date = request.POST.get('due_date')
        print(date)
        if date == "":
            project = Project(project_name=name)
        else:
            project = Project(project_name=name,due_date=date)        
        project.save()
        return HttpResponseRedirect('/manager_tools')



    form = projectForm()
    return render(request, 'create_project.html', {'form':form})


def home_page(request, employee_id, day, month, year):
    screen_date = date(year,month,day)
    employee = Employee.objects.get(pk=employee_id)
    shift = employee.Shifts.filter(date=screen_date)
    if shift.first() != None:
        shift = shift.first()
    # should filter all tasks that have not been completed
    # date from url
    print(shift)
    print(screen_date)
    tasks =  employee.Tasks.filter(is_complete=False, date_assigned_to__range=( date.min, screen_date)) 
   #print(employee)
   # print(tasks)
    

    if request.method == 'POST':
        # go through the tasks and find the object that was selected and clock in or out
        # I just have the buttons named as the task object they are associated with
        print(request.POST)
       
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
            
            elif str(x) + " complete" in request.POST:
                x.is_complete = True
                x.save()

    return render(request, 'home_page.html',{ 'employee':employee, 'tasks':tasks, 'shift':shift})

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
    if request.method == 'POST':
        
        form = employeeIdSearch(request.POST)
        
        if form.is_valid():
           
            input_id = form.cleaned_data['employee_id'].strip()
            if (not is_valid_id(input_id)):
                return render(request, 'employee_stats.html', {'form' : form,
                                                                'show_error': True})


            # get tasks
            employee = Employee.objects.get(employee_id=input_id)
            tasks = employee.Tasks.all()
            name = f'{employee.user.first_name} {employee.user.last_name}' 
            return render(request, 'employee_stats.html', {'form': form, 
                                                           'tasks': tasks, 
                                                           'employee': employee,
                                                           'employee_name': name})
    else:
        form = employeeIdSearch()

    return render(request, 'employee_stats.html', {'form' : form })



"""
    Add Task
"""

def add_task(request):
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

            print(employee)
            if employee != None:
                employee.Tasks.add(newTask)
                message = "You have been assigned a new task: " + str(newTask.task_name)
                channel_layer = get_channel_layer()
                # Trigger message sent to group
                async_to_sync(channel_layer.group_send)(
                    str(employee.pk), # uses an employees primary key
                    {
                        "type": "send_notification",
                        "message": message
                    }
                )

            return HttpResponseRedirect('/manager_tools')
    else:
        form = addTask()

    return render(
    request, 
    'add_task.html',
    {'form': form}
    )


'''
Employee will need to be changed to allow for multiple employees to appear
'''




def edit_task(request, task_id):

    task = Task.objects.get(pk=task_id) 
    if request.method=='POST':
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

            # Used for notifications
                message = "Your task '" + str(task.task_name) + "' has been edited"
                channel_layer = get_channel_layer()
                # Trigger message sent to group
                async_to_sync(channel_layer.group_send)(
                    str(employee.pk), # uses an employees primary key
                    {
                        "type": "send_notification",
                        "message": message
                    }
                )

            task.save()
            # Going to loop through each field to make sure its not empty
            

        return HttpResponseRedirect('/manager_tools')
   
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


    form = updateTask()
    return render(request, 'update_task_status.html', {'form':form})

