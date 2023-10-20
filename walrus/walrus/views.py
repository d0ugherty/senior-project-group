from django import forms
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse

from .models import Tasks
from .forms import taskSearchForm
def list_tasks(request):
    try:
        tasks = Tasks.objects.all()
    except: 
        raise Http404('No Tasks Found')
    
    form = taskSearchForm()
    return render(request, 'task_list.html', {
        'tasks': tasks, 'form':form
    })