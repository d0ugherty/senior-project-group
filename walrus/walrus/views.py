from django import forms
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse

from .models import *
from .forms import taskSearchForm
def list_tasks(request):
    try:
        tasks = Task.objects.all()
    except: 
        raise Http404('No Tasks Found')
    


    if request.method == "POST":
        task_name = request.POST.get('task_name')
        project_name = request.POST.get('project_name')
        due_date = request.POST.get('due_date')
        status = request.POST.get('status')

        if status == "complete":
           status = True
        elif status == "incomplete":
           status = False
        else: 
            status = ""


        if (Project.objects.filter(project_name=project_name).exists()):
         project_object = Project.objects.get(project_name=project_name)
        else: project_object = ""
         
        fields ={
                    'task_name': task_name,
                    'project': project_object,
                    'is_complete': status
            }
         #print(fields)
         
        nonEmptyFields = {}
        for x in fields:
         if fields[x] != "":
          nonEmptyFields.update({x : fields[x]})
        
         

         #print(fields)
        print(nonEmptyFields)
        print(Task.objects.filter(**nonEmptyFields))
        Task.objects.filter(**nonEmptyFields)
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