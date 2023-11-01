
from django import forms
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.urls import reverse
import datetime
from datetime import datetime, timedelta
from calendar import month_name
from calendar import HTMLCalendar

from .models import Task
from .forms import taskSearchForm, addTask, employeeIdSearch
from .util import *

from datetime import datetime,timezone

# after user logs in this redirects them to home page
def home_redirect(request):
    user=request.user
    if user.is_authenticated:
        url = 'home/' + str(user.employee.pk)
        return redirect(url)
    return render(request, 'home.html')


def list_tasks(request):
   # try:
        #tasks = Task.objects.all()
    #except: 
    #    raise Http404('No Tasks Found')
    tasks = None


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

def home_page(request, employee_id):


    '''
    todays_date = datetime.date.today() # todays date
    todays_date=todays_date-datetime.timedelta(40) # going back a certain amount of days
    # todays_date=date.today().weekday() # week day as an int
    todays_date=todays_date.weekday()
    '''
    employee = Employee.objects.get(pk=employee_id)

    # should filter all tasks that have not been completed
    tasks =  employee.Tasks.filter()
   #print(employee)
   # print(tasks)
    test = 1
    if request.method == 'POST':
        # go through the tasks and find the object that was selected and clock in or out
        # I just have the buttons named as the task object they are associated with
        #print(request.POST)
       
        for x in tasks:
            #print (str(x) + "complete")

            if str(x) in request.POST:
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



    return render(request, 'home_page.html',{ 'employee':employee, 'tasks':tasks, 'test':test})



def calendar(request):
    curMonth = datetime.now().month
    curYear = datetime.now().year
    curCalen =  HTMLCalendar().formatmonth(curYear, curMonth)
    tasks = Task.objects.all()
    return render(request, 'calendar.html', {
        'curCalen': curCalen,
        'tasks': tasks
    })

def add_task(request):
    if request.method=='POST':
        form = addTask(request.POST)
        if form.is_valid():
            task_name = form.cleaned_data['task_name']
            task_description = form.cleaned_data['description']
            newTask = Task(
                task_name = task_name,
                task_description = task_description,
            )

            newTask.save()
            return HttpResponseRedirect('/calendar')
    else:
        form = addTask()

    return render(
    request, 
    'add_task.html',
    {'form': form}
    )

def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return HttpResponseRedirect(reverse('calendar'))

"""
    Loads the manager home page
    TO DO: Check for user type
"""
def load_manager_home(request):
    return render(request, 'manager_home.html')

"""
    Retrieves the 'destination' name of a button
    on the Manager Home page and 
    Redirects the user to the appropriate page 
    according to the 'destionation' string

    Currently, the un-implemented pages will default to "invalid destination"

    TO DO: Add more redirects as project progresses
"""
def manager_home_redirect(request):
    destination = request.POST.get('destination')
    match destination:
        case "/add_task/":
            return HttpResponseRedirect(destination)
        case "/list_tasks/":
            return HttpResponseRedirect(destination)
        case "/employee_stats/":
            return HttpResponseRedirect(destination)
        case _:
            return HttpResponse("Invalid destination", status=400)

"""
    View for the loading employee stats page

    search_input is a CharField form and employee_id is an integer type
    in the database. so validate_id checks if the input is a digit and if so 
    casts the input as an integer
"""
def employee_stats(request):
    if request.method == 'POST':
        form = employeeIdSearch(request.POST)
        if form.is_valid():
            employee_id = form.cleaned_data['employee_id'].strip()
            validate_id(employee_id, form)
            print("id has been submitted")
            return HttpResponseRedirect('employee_stats', employee=employee_id)
    else:
        form = employeeIdSearch()

    return render(request, 'employee_stats.html', {'form' : form })