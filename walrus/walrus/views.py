
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
from .forms import taskSearchForm, addTask, employeeIdSearch, updateTask
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

class CalendarView(generic.ListView):
    model = Task
    template_name = 'calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('day', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        return context

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

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
            validate_id(input_id, form)

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

