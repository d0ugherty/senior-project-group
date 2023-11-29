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
from .forms import *
from .util import *

from datetime import datetime,timezone

from django.contrib import messages
# Imports for notifications
from walrus.admin import SendNotificationForm
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync



def availability(request, employee_id):
    print("hello")
    employee = Employee.objects.get(pk=employee_id)
    if request.method == "POST":
        employee = Employee.objects.get(pk=employee_id)
        if employee.availability == None:
                #print("does not")
                availability = Availability()
                availability.save()
                employee.availability = availability
                employee.save()
        set_availability(request, employee)
        # returning to home page
        today = datetime.today()
        return HttpResponseRedirect('/home/' + str(employee_id) + '/' + str(today.day) + '/' + str(today.month) + '/' + str(today.year))

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
#    page = 'home/' + str(request.user.pk)
    #redirect('page')


    form = availabilityForm(initial=dict)
    return render(request, 'availability.html', {'form':form})

def request_time_off(request, employee_id):
    user = request.user
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

    # getting and changing the profile pic
    if request.method == 'POST':
        print(request.POST)
        if 'change picture' in request.POST:
            form = change_profile_image_Form(request.POST, request.FILES)
            if form.is_valid():
                image = form.cleaned_data.get('profile_pic')
                user.employee.profile_pic = image
                user.employee.save()
        if 'remove' in request.POST:
            user.employee.profile_pic = None
            user.employee.save()


    
    pic_form = change_profile_image_Form()
    #return render (request, 'profile.html', {'user':user, 'pic_form':pic_form})
    return render (request, 'new_profile.html',{'user':user})
    #return render (request, 'edit_profile.html',{'user':user})

def edit_profile(request, employee_id):
    user = request.user
    if request.method == 'POST':
        form = change_profile_image_Form(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data.get('profile_pic')
            print(image)
            if image != None:
                user.employee.profile_pic = image
                user.employee.save()
        print("hello")
        print(request.POST)    
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        # PUT PHONE NUMBER AND IMAGE



        print(first_name)
        print(user.first_name)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.employee.phone_number = phone_number
        user.employee.save()
        user.save()
        
    pic_form = change_profile_image_Form()
    return render (request, 'edit_profile.html',{'user':user, 'form':pic_form})
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
    user = request.user
    if user.employee.is_manager == 'No':
         return render(request, 'notAManager.html')


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


def task_detail (request, task_id):
    form = taskSearchForm()

    task = Task.objects.get(id=task_id)
    employees = task.employee_set.all()
    updates = task.task_update_set.all()
    print(updates)
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
    print(shift)
    print(screen_date)
    tasks =  employee.Tasks.filter(is_complete=False, date_assigned_to__range=( date.min, screen_date), wont_complete = False) 
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
                print(str(x) + " complete")
                x.is_complete = True
                x.save()
                return redirect('home')
               

#    if request.htmx:
 #       return render(request, 'post/partials/bitcoin.html',{ 'employee':employee, 'tasks':tasks, 'shift':shift})

  #  else:


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
           
            input_id = form.cleaned_data['employee_id'].strip()
            if (not is_valid_id(input_id)):
                return render(request, 'employee_stats.html', {'form' : form,
                                                                'show_error': True})
            # get tasks
            print(input_id)
            
            if  (Employee.objects.filter(pk=input_id)):
                employee = Employee.objects.get(pk=input_id)
                
                tasks = employee.Tasks.all()
                name = f'{employee.user.first_name} {employee.user.last_name}' 
                time_spent = []
                for t in tasks:
                    if (Time_Spent.objects.filter(employee=employee.pk,task=t.pk)):
                       time_record = Time_Spent.objects.get(employee=employee.pk,task=t.pk)
                       time_spent.append(time_record.total_time)
                    else:
                       time_spent.append(None)
                print(time_spent)


                return render(request, 'employee_stats.html', {'form': form, 
                                                            'tasks': tasks, 
                                                            'employee': employee,
                                                            'employee_name': name,
                                                            'time_spent' : time_spent})
    else:
        form = employeeIdSearch()
    return render(request, 'employee_stats.html', {'form' : form })

"""
    Create Role
"""
def create_role(request):
    if request.method == 'POST':
        form = createRole(request.POST)
        if form.is_valid():
            role_name = form.cleaned_data['role_name'].strip()
            role_desc = form.cleaned_data['description'].strip()
            ## prevent duplicates by checking if a role with the same name exists
            if not is_valid_role(role_name):
                # show error
                pass
            else:
                new_role = Role.objects.create(name=role_name, description=role_desc)
            return render(request, 'create_role.html', {'form': form,
                                                        'role': new_role})
    else:
        form = createRole()
        return render(request,'create_role.html',{'form' : form})

"""
    Add Task
"""

def add_task(request):
    user = request.user
    if user.employee.is_manager == 'No':
         return render(request, 'notAManager.html')
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

    user = request.user
    if user.employee.is_manager == 'No':
         return render(request, 'notAManager.html')


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
            

        return HttpResponseRedirect('/task_detail/' + str(task_id))
   
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
        print("we at post")
        form = updateTask(request.POST, request.FILES)
        if form.is_valid():
            description = request.POST.get('description')
            image = form.cleaned_data.get('image')
            print("HELA")
            print(image)
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
        if "search" in request.POST:
            form = employeeDropdownSearch(request.POST)
            if form.is_valid():
                employee = form.cleaned_data['employee']
               
                print(employee.pk)
                avil = employee.availability
                print(avil)
                print(datetime.today())
                requests_off = employee.Request_Offs.filter(start__range=(datetime.today(), (datetime.today()+ timedelta(10000))))
        if "save_shift" in request.POST:
            employee_pk = request.POST.get('employee')
            employee = Employee.objects.get(pk=employee_pk)
            date = request.POST.get('date')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            print(employee)
            shift = Shift(date=date, start=start_time, end=end_time)
            shift.save()
            employee.Shifts.add(shift)
        if "select_week_form" in request.POST:
            form = selectWeek(request.POST)
            if form.is_valid():
                date = form.cleaned_data['date']
                print(date.weekday())
                
                start_date = None
                end_date = None
                if (date.weekday() == 0):
                    start_date = date-timedelta(1)
                    end_date = date + timedelta(5)

                    print(start_date)
                    print(end_date)
                if (date.weekday() == 1):
                    start_date = date-timedelta(2)
                    end_date = date + timedelta(4)

                    print(start_date)
                    print(end_date)

                if (date.weekday() == 2):
                    start_date = date-timedelta(3)
                    end_date = date + timedelta(3)

                    print(start_date)
                    print(end_date)
                if (date.weekday() == 3):
                    start_date = date-timedelta(4)
                    end_date = date + timedelta(2)

                    print(start_date)
                    print(end_date)
                if (date.weekday() == 4):
                    start_date = date-timedelta(5)
                    end_date = date + timedelta(1)

                    print(start_date)
                    print(end_date)
                if (date.weekday() == 5):
                    start_date = date-timedelta(6)
                    end_date = date 
                    print(start_date)
                    print(end_date)
                if (date.weekday() == 6):
                    start_date = date
                    end_date = date + timedelta(6)


                #    print(start_date)
               #     print(end_date)
            shiftsThisWeek = Shift.objects.filter(date__range=(start_date, (end_date + timedelta(1)))).order_by('date')
            
            #for i in shifts:
            # print(i.day_of_week())
            employees = Employee.objects.all()
        '''
            for e in employees:
                print(e)
                list = []
                list.append(e)
                for s in shiftsThisWeek:
                        if s in e.Shifts.all():
                            #print("found a shift")
                            list.append(s)
                dict[str(e.pk)] = (list) 
            '''
        for e in employees:
                print(e)
                list = [None, None, None, None, None, None, None,None]
                list[0]=e
                for s in shiftsThisWeek:
                        if s in e.Shifts.all():
                            temp = s.day_of_week()
                            if temp == 6:
                                list[1] = s
                            if temp == 0:
                                list[2] = s
                            if temp == 1:
                                list[3] = s
                            if temp == 2:
                                list[4] = s
                            if temp == 3:
                                list[5] = s
                            if temp == 4:
                                list[6] = s
                            if temp == 5:
                                list[7] = s

                dict[str(e.pk)] = (list) 
        
                #print (dict)
            #print(shifts)
            #print(employees)

            #Restructruring data

            


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
        form = failureForm(request.POST)
        task = Task.objects.get(id=task_id)
        if form['failure']:
            task.wont_complete = True
        task.save()
        return HttpResponseRedirect(reverse('list_tasks'))
    
    form = failureForm()
    return render(request, 'task_failure.html',
                  { 'fail_form':form })
