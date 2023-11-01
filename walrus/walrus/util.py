from calendar import HTMLCalendar
from .models import * 
import datetime
from datetime import datetime,timezone, timedelta

def find_tasks(task_name, project_name, due_date, status):
    if status == "complete":
           status = True
    elif status == "incomplete":
           status = False
    else: 
            status = ""

     
   
    if (project_name != "" and Project.objects.filter(project_name=project_name).exists()==False):
         return None
    if (Project.objects.filter(project_name=project_name).exists()):
         project_object = Project.objects.get(project_name=project_name)
    else: project_object = ""
         
    fields ={
                    'task_name': task_name,
                    'project': project_object,
                    'is_complete': status,
                    'due_date': due_date
            }
         #print(fields)
         
    nonEmptyFields = {}
    for x in fields:
        if fields[x] != "":
          nonEmptyFields.update({x : fields[x]})
        #this is a test

         #print(fields)
    print(nonEmptyFields)
    print(Task.objects.filter(**nonEmptyFields))
    tasks = Task.objects.filter(**nonEmptyFields)
    return tasks
"""
     IDs are being input as CharFields, this will
     just help to make sure that data entered is valid
"""
def validate_id(input_id, form):
     id_str = input_id.strip()
     if id_str.isdigit():
          return int(id_str)
     else:
          form.add_error('employee_id', 'Please enter a valid ID')

def adjust_clock_in(time_record):
                    print("boo")
                    # When employee clocks in 
                    if (time_record.in_progress == False):
                        time_record.in_progress=True
                        time_record.last_clock_in = datetime.now()
                        time_record.last_clock_in = datetime.now(timezone.utc)
                        time_record.save()
                        print("clock")
                    else:
                    # When employee clocks out 

                        additionalTime = datetime.now(timezone.utc) - time_record.last_clock_in
                        print(additionalTime)
                        time_record.total_time = time_record.total_time + additionalTime
                       
                        time_record.in_progress = False
                        time_record.save()
                        print("clock2")