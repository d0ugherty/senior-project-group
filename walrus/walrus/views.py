
from django import forms
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
import datetime
from datetime import datetime
from calendar import month_name
from calendar import HTMLCalendar

from .models import Task
from .forms import taskSearchForm
from .util import *
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

def calendar(request):
    curMonth = datetime.now().month
    curYear = datetime.now().year
    curCalen =  HTMLCalendar().formatmonth(curYear, curMonth)
    return render(request, 'calendar.html', {
        'curCalen': curCalen,
    })