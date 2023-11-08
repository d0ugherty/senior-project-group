from datetime import datetime, timedelta
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
  
class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter tasks by day
	def formatday(self, day, tasks):
		tasks_per_day = tasks.filter(date_created__day=day)
		d = ''
		for task in tasks_per_day:
			d += f'<li> {task.task_name} </li>'

		if day != 0:
			return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
		return '<td></td>'

	# formats a week as a tr 
	def formatweek(self, theweek, tasks):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, tasks)
		return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter tasks by year and month
	def formatmonth(self, withyear=True):
		tasks = Task.objects.filter(date_created__year=self.year, date_created__month=self.month)

		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, tasks)}\n'
		return cal

"""
     IDs are being input as CharFields, this will
     just help to make sure that data entered is valid
"""
def is_valid_id(input_id):
       return input_id.strip().isdigit()
     

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

def set_availability(request,employee):
     print("called")
            
     employee.availability.sunday_start = request.POST.get('sunday_start')
     employee.availability.sunday_end = request.POST.get('sunday_end')

     employee.availability.monday_start = request.POST.get('monday_start')
     employee.availability.monday_end = request.POST.get('monday_end')

     employee.availability.tuesday_start = request.POST.get('tuesday_start')
     employee.availability.tuesday_end = request.POST.get('tuesday_end')

     employee.availability.wednesday_start = request.POST.get('wednesday_start')
     employee.availability.wednesday_end = request.POST.get('wednesday_end')

     employee.availability.thursday_start = request.POST.get('thursday_start')
     employee.availability.thursday_end = request.POST.get('thursday_end')

     employee.availability.friday_start = request.POST.get('friday_start')
     employee.availability.friday_end = request.POST.get('friday_end')

     employee.availability.saturday_start = request.POST.get('saturday_start')
     employee.availability.saturday_end = request.POST.get('saturday_end')

     #print( employee.availability.sunday_start)
     employee.availability.save()
     #print(sunday_start)



