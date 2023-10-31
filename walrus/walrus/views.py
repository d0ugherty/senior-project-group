from django import forms
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse

from .models import *
from .forms import taskSearchForm
from .util import *

from datetime import datetime,timezone
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
              
                #Getting the Time_spent object associated with the task and employee
                if (Time_Spent.objects.filter(employee=employee_id,task=x.pk)):
                    time_record = Time_Spent.objects.get(employee=employee_id,task=x.pk)
           
                    # When employee clocks in 
                    if (time_record.in_progress == False):
                        time_record.in_progress=True
                        time_record.last_clock_in = datetime.now()
                        time_record.last_clock_in = datetime.now(timezone.utc)
                        time_record.save()
                    else:
                    # When employee clocks out 

                        additionalTime = datetime.now(timezone.utc) - time_record.last_clock_in
                        time_record.total_time = time_record.total_time + additionalTime
                       
                        time_record.in_progress = False
                        time_record.save()


    return render(request, 'home_page.html',{ 'employee':employee, 'tasks':tasks, 'test':test})

