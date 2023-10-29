
from django import forms
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
import datetime
from datetime import datetime, timedelta
from calendar import month_name
from calendar import HTMLCalendar

from .models import Task
from .forms import taskSearchForm, addTask, updateTask
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