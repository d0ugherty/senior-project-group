from .models import * 

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