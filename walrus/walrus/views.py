from django import forms
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse

from .models import *
from .forms import taskSearchForm
from .util import *

import datetime
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

def home_page(request):



    todays_date = datetime.date.today() # todays date
    todays_date=todays_date-datetime.timedelta(40) # going back a certain amount of days
    # todays_date=date.today().weekday() # week day as an int
    todays_date=todays_date.weekday()
    return render(request, 'home_page.html',{'date':todays_date} )

