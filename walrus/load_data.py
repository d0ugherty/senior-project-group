import os
import django
import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'walrus.settings')
django.setup()

#from walrus.views import *
#from .models import Employee
from django.contrib.auth.models import User
from walrus.models import Employee, Task, Project, Task_Update, Time_Spent, Availability, Shift
Availability.objects.all().delete()
Time_Spent.objects.all().delete()
Task_Update.objects.all().delete()
Employee.objects.all().delete()
User.objects.all().delete()
Project.objects.all().delete()
Task.objects.all().delete()
Shift.objects.all().delete()
# Update 1
update_1 = Task_Update(description="Task has been started")
update_1.save()
# Update 2
update_2 = Task_Update(description="Task is 50 percent done", venue_image="/images/entrance_display.jpg")
update_2.save()
# Project 1
project = Project(project_name="Display")
project.save()
project2 = Project(project_name="Truck")
project2.save()


# Task 1
task = Task()
task.task_name="set up entrance display"
task.task_description="At the entrance of the store, prepare the new seasonal display."
task.project = project
task.date_assigned_to = '2023-12-05 09:30:59'
task.due_date = '2023-12-19'

task.save()

task.task_update_set.add(update_1)
task.task_update_set.add(update_2)



# Task 2
task2 = Task()
task2.task_name="unload Truck"
task2.project = project2
task2.save()


"""
    These tasks can be part of the same Project

"""

# Task 3
# This task is complete 
task3 = Task()
task3.task_name = "Setup Christmas light display"
task3.is_complete = True
task3.date_created = '2023-12-05 11:25:20'
task3.date_assigned_to = '2023-12-05 09:30:59'
task3.due_date = '2023-12-21'
task3.date_completed = '2023-12-05 14:13:27'
task3.save()

# Task 4
# This task is in progress
task4 = Task()
task4.task_name = "Setup reindeer display"
task4.date_created = '2023-12-05 11:25:20'
task4.date_assigned_to = '2023-12-05 09:30:59'
task4.due_date = '2023-12-20'
task4.date_completed = None
task4.is_complete = False
task4.save()

#Task 5
task5 = Task()
task5.task_name = "Setup Santa Clause display"
task5.date_created = '2023-12-02 1:25:20'
task5.date_assigned_to = '2023-12-05 09:30:59'
task5.due_date = '2023-12-20'
task5.date_completed = None
task5.is_complete = False
task5.to_be_taken= True
task5.save()

#Task6 
task6 = Task()
task6.task_name="Update Registers"
task6.task_description="Registers have a new update. Please restart the systems."
task6.date_assigned_to = '2023-12-10 09:30:59'
task6.due_date = '2023-12-23'

task6.save()


today = datetime.datetime.today()

# shift 1

shift_1 = Shift(date=today, start="7:00am", end="12:00pm")
shift_1.to_be_taken=True
shift_1.save()

# Shift 2
shift_2 = Shift(date=today + datetime.timedelta(days=1), 
                start="8:00am", 
                end="1:00pm")
shift_2.to_be_taken = True
shift_2.save()

# Shift 3
shift_3 = Shift(date=today + datetime.timedelta(days=2), 
                start="9:00am", 
                end="2:00pm")
shift_3.to_be_taken = True
shift_3.save()

# Shift 4
shift_4 = Shift(date=today + datetime.timedelta(days=3), 
                start="10:00am", 
                end="3:00pm")
shift_4.to_be_taken = True
shift_4.save()

# Shift 5
shift_5 = Shift(date=today + datetime.timedelta(days=4), 
                start="11:00am", 
                end="4:00pm")
shift_5.to_be_taken = True
shift_5.save()

# Shift 6
shift_6 = Shift(date=today + datetime.timedelta(days=5), 
                start="12:00pm", 
                end="5:00pm")
shift_6.to_be_taken = True
shift_6.save()

# User/Employee 1
user = User.objects.create_user(username="test", 
                                email="oconno65@students.rowan.edu", 
                                password="test", 
                                is_staff=True)
user.first_name = "John"
user.last_name = "Smith"
user.is_superuser = True
user.save()
e = Employee(user=user, employee_id = 1)

e.save()
e.is_manager = "Yes"
e.Tasks.add(task)
e.Tasks.add(task2)
e.Tasks.add(task6)
e.Shifts.add(shift_1)
# avil
availability = Availability(sunday_start='Not available', sunday_end = 'Not available', monday_start = '7:00am', monday_end = '12:00pm')
availability.save()
e.availability =  availability
print(e.availability)
e.save()
# User/Employee 2
user = User.objects.create_user(username="john", 
                                email="lennon@thebeatles.com", 
                                password="johnpassword", 
                                is_staff=True)
user.is_superuser = True
user.first_name = "Matt"
user.last_name = "Smith"
user.save()
e = Employee(user=user, employee_id = 2)

e.save()
e.Tasks.add(task3)
e.Tasks.add(task4)
e.Tasks.add(task5)
# User/Employee 3

user20 = User.objects.create_user(username="walker", 
                                email="doughe38@students.rowan.edu", 
                                password = "password",
                                is_staff=True)
user20.first_name = "Walker"
user20.last_name = "Texas Ranger"
user20.is_superuser = True
user20.save()

e20 = Employee(user=user20, employee_id = 2)
e20.save()


user1 = User.objects.create_user(username="user1", 
                                email="doughe38@students.rowan.edu", 
                                password = "password",
                                is_staff=True)
user1.first_name = "Johnny"
user1.last_name = "Cash"
user1.is_superuser = False
user1.save()


e1 = Employee(user=user1, employee_id = 4)
e1.save()

user2 = User.objects.create_user(username="user2", 
                                email="doughe38@students.rowan.edu", 
                                password = "password",
                                is_staff=True)
user2.first_name = "Merle"
user2.last_name = "Haggard"
user2.is_superuser = False
user2.save()


e2 = Employee(user=user2, employee_id = 5)
e2.save()

user3 = User.objects.create_user(username="user3", 
                                email="doughe38@students.rowan.edu", 
                                password = "password",
                                is_staff=True)
user3.first_name = "Kris"
user3.last_name = "Kristofferson"
user3.is_superuser = False
user3.save()


e3 = Employee(user=user3, employee_id = 6)
e3.save()

user4 = User.objects.create_user(username="user4", 
                                email="doughe38@students.rowan.edu", 
                                password = "password",
                                is_staff=True)
user4.first_name = "Willie"
user4.last_name = "Nelson"
user4.is_superuser = False
user4.save()


e4 = Employee(user=user4, employee_id = 7)
e4.save()

# User 8
user8 = User.objects.create_user(username="user8",
                                 email="lucy.meadows@outlook.com",
                                 password="password",
                                 is_staff=False)
user8.first_name = "Lucy"
user8.last_name = "Meadows"
user8.is_superuser = False
user8.save()

e5 = Employee(user=user8, employee_id = 8)
e5.save()


# User 9
user9 = User.objects.create_user(username="user9",
                                 email="james.bond@mi6.gov",
                                 password="password",
                                 is_staff=True)
user9.first_name = "James"
user9.last_name = "Bond"
user9.is_superuser = True
user9.save()

e6 = Employee(user=user9, employee_id = 9)
e6.save()


# User 10
user10 = User.objects.create_user(username="user10",
                                  email="emma.watson@fanmail.com",
                                  password="password",
                                  is_staff=False)
user10.first_name = "Emma"
user10.last_name = "Watson"
user10.is_superuser = False
user10.save()

e7 = Employee(user=user10, employee_id = 10)
e7.save()


# User 11
user11 = User.objects.create_user(username="user11",
                                  email="mark.twain@literature.com",
                                  password="password",
                                  is_staff=True)
user11.first_name = "Mark"
user11.last_name = "Twain"
user11.is_superuser = False
user11.save()

e8 = Employee(user=user11, employee_id = 11)
e8.save()


# User 12
user12 = User.objects.create_user(username="user12",
                                  email="sophia.lopez@musicworld.org",
                                  password="password",
                                  is_staff=False)
user12.first_name = "Sophia"
user12.last_name = "Lopez"
user12.is_superuser = True
user12.save()

e9= Employee(user=user12, employee_id = 12)
e9.save()

# User 11
user13 = User.objects.create_user(username="user13",
                                  email="mark.twain@literature.com",
                                  password="password",
                                  is_staff=True)
user13.first_name = "Mark"
user13.last_name = "Twain"
user13.is_superuser = False
user13.save()

e10 = Employee(user=user13, employee_id = 13)
e10.save()

# Availability 1
availability1 = Availability(
    sunday_start="9:00am", sunday_end="5:00pm",
    monday_start="8:00am", monday_end="4:00pm",
    tuesday_start='Not available', tuesday_end='Not available',
    wednesday_start="9:00am", wednesday_end="5:00pm",
    thursday_start="8:00am", thursday_end="4:00pm",
    friday_start="9:00am", friday_end="5:00pm",
    saturday_start='Not available', saturday_end='Not available'
)
availability1.save()
e1.availability = availability1
e1.save()

# Availability 2
availability2 = Availability(
    sunday_start="10:00am", sunday_end="6:00pm",
    monday_start="9:00am", monday_end="5:00pm",
    tuesday_start="10:00am", tuesday_end="6:00pm",
    wednesday_start='Not available', wednesday_end='Not available',
    thursday_start="9:00am", thursday_end="5:00pm",
    friday_start='Not available', friday_end='Not available',
    saturday_start="10:00am", saturday_end="6:00pm"
)

availability2.save()
e2.availability = availability2
e2.save()

# Availability 3
availability3 = Availability(
    sunday_start='Not available', sunday_end='Not available',
    monday_start="8:00am", monday_end="4:00pm",
    tuesday_start="9:00am", tuesday_end="5:00pm",
    wednesday_start="8:00am", wednesday_end="4:00pm",
    thursday_start='Not available', thursday_end='Not available',
    friday_start="9:00am", friday_end="5:00pm",
    saturday_start="8:00am", saturday_end="4:00pm"
)
availability3.save()
e3.availability = availability3
e3.save()

# Availability 4
availability4 = Availability(
    sunday_start="7:00am", sunday_end="3:00pm",
    monday_start='Not available', monday_end='Not available',
    tuesday_start="7:00am", tuesday_end="3:00pm",
    wednesday_start='Not available', wednesday_end='Not available',
    thursday_start="7:00am", thursday_end="3:00pm",
    friday_start='Not available', friday_end='Not available',
    saturday_start="7:00am", saturday_end="3:00pm"
)
availability4.save()

e4.availability = availability4
e4.save()

# Availability 5
availability5 = Availability(
    sunday_start='Not available', sunday_end='Not available',
    monday_start="10:00am", monday_end="6:00pm",
    tuesday_start='Not available', tuesday_end='Not available',
    wednesday_start="10:00am", wednesday_end="6:00pm",
    thursday_start='Not available', thursday_end='Not available',
    friday_start="10:00am", friday_end="6:00pm",
    saturday_start='Not available', saturday_end='Not available'
)
availability5.save()

e5.availability = availability5
e5.save()

# Availability 6
availability6 = Availability(
    sunday_start="11:00am", sunday_end="7:00pm",
    monday_start="12:00pm", monday_end="8:00pm",
    tuesday_start='Not available', tuesday_end='Not available',
    wednesday_start='Not available', wednesday_end='Not available',
    thursday_start="12:00pm", thursday_end="8:00pm",
    friday_start="11:00am", friday_end="7:00pm",
    saturday_start="9:00am", saturday_end="5:00pm"
)
availability6.save()

e20.availability = availability6
e6.save()

# Availability 7
availability7 = Availability(
    sunday_start='Not available', sunday_end='Not available',
    monday_start="7:00am", monday_end="3:00pm",
    tuesday_start="8:00am", tuesday_end="4:00pm",
    wednesday_start='Not available', wednesday_end='Not available',
    thursday_start="7:00am", thursday_end="3:00pm",
    friday_start="8:00am", friday_end="4:00pm",
    saturday_start='Not available', saturday_end='Not available'
)
availability7.save()
e7.availability = availability7
e7.save()

# Availability 8
availability8 = Availability(
    sunday_start="9:00am", sunday_end="5:00pm",
    monday_start='Not available', monday_end='Not available',
    tuesday_start="9:00am", tuesday_end="5:00pm",
    wednesday_start='Not available', wednesday_end='Not available',
    thursday_start="9:00am", thursday_end="5:00pm",
    friday_start='Not available', friday_end='Not available',
    saturday_start="10:00am", saturday_end="6:00pm"
)
availability8.save()

e8.availability = availability8
e8.save()

# Availability 9
availability9 = Availability(
    sunday_start='Not available', sunday_end='Not available',
    monday_start="10:00am", monday_end="6:00pm",
    tuesday_start='Not available', tuesday_end='Not available',
    wednesday_start="10:00am", wednesday_end="6:00pm",
    thursday_start='Not available', thursday_end='Not available',
    friday_start="10:00am", friday_end="6:00pm",
    saturday_start='Not available', saturday_end='Not available'
)
availability9.save()
e9.availability = availability9
e9.save()

# Availability 10
availability10 = Availability(
    sunday_start="8:00am", sunday_end="4:00pm",
    monday_start="9:00am", monday_end="5:00pm",
    tuesday_start="8:00am", tuesday_end="4:00pm",
    wednesday_start='Not available', wednesday_end='Not available',
    thursday_start="9:00am", thursday_end="5:00pm",
    friday_start="8:00am", friday_end="4:00pm",
    saturday_start='Not available', saturday_end='Not available'
)
availability10.save()

#e10.availability = availability10

# Project 3 - Inventory Management
project3 = Project(project_name="Inventory Management")
project3.save()

# Related Tasks for Project 3
task12 = Task(task_name="Audit Inventory", task_description="Conduct a thorough audit of store inventory.", project=project3)
task12.save()
e1.Tasks.add(task12)

task13 = Task(task_name="Update Inventory System", task_description="Update the electronic inventory management system.", project=project3)
task13.save()
e1.Tasks.add(task13)

task14 = Task(task_name="Order New Stock", task_description="Identify and order new stock as per inventory needs.", project=project3)
task14.save()
e1.Tasks.add(task14)

e1.save()
# Project 4 - Staff Training
project4 = Project(project_name="Staff Training")
project4.save()

# Related Tasks for Project 4
task15 = Task(task_name="Develop Training Material", task_description="Develop new material for staff training.", project=project4)
task15.save()
e2.Tasks.add(task15)
task16 = Task(task_name="Schedule Training Sessions", task_description="Schedule and organize training sessions for staff.", project=project4)
task16.save()
e2.Tasks.add(task16)
task17 = Task(task_name="Evaluate Training Outcomes", task_description="Evaluate the effectiveness of the training sessions.", project=project4)
task17.save()
e2.Tasks.add(task17)
e2.save()

# Project 6 - Garden Center Revamp
project6 = Project(project_name="Garden Center Revamp")
project6.save()

# Related Tasks for Project 6
task21 = Task(task_name="Restock Garden Supplies", task_description="Ensure all gardening tools and supplies are fully stocked.", project=project6)
task21.save()
e3.Tasks.add(task21)
task22 = Task(task_name="Update Plant Display", task_description="Redesign the display area for seasonal plants and flowers.", project=project6)
task22.save()
e3.Tasks.add(task22)
task23 = Task(task_name="Organize Outdoor Furniture", task_description="Arrange and showcase the new range of outdoor furniture.", project=project6)
task23.save()
e3.Tasks.add(task23)
e3.save()

# Project 7 - Paint Department Overhaul
project7 = Project(project_name="Paint Department Overhaul")
project7.save()

# Related Tasks for Project 7
task24 = Task(task_name="Conduct Paint Inventory", task_description="Perform a detailed inventory check in the paint department.", project=project7)
task24.save()
e4.Tasks.add(task24)
e4.save()

task25 = Task(task_name="Set Up Color Mixing Station", task_description="Establish a new color mixing station for custom paint orders.", project=project7)
task25.save()
e5.Tasks.add(task25)
e5.save()
task26 = Task(task_name="Train Staff on New Paint Products", task_description="Train the staff on the features of new paint products.", project=project7)
task26.save()
e6.Tasks.add(task26)
e6.save()

# Project 8 - Tool Rental Service Expansion
project8 = Project(project_name="Tool Rental Service Expansion")
project8.save()

# Related Tasks for Project 8
task27 = Task(task_name="Inspect Rental Tools", task_description="Inspect and perform maintenance on all rental tools.", project=project8)
task27.save()
e7.Tasks.add(task27)
task28 = Task(task_name="Update Rental Catalog", task_description="Update the tool rental catalog with new additions and remove outdated items.", project=project8)
task28.save()
e7.Tasks.add(task28)
e7.save()
task29 = Task(task_name="Enhance Online Rental Process", task_description="Improve the online tool rental process for better customer experience.", project=project8)
task29.save()
e8.Tasks.add(task29)


# Shift 7 for Employee e1
shift_7 = Shift(date=today + datetime.timedelta(days=1), 
                start="9:00am", 
                end="2:00pm")
shift_7.to_be_taken = True
shift_7.save()
e1.Shifts.add(shift_7)
e1.save()

# Shift 8 for Employee e2
shift_8 = Shift(date=today + datetime.timedelta(days=2), 
                start="10:00am", 
                end="3:00pm")
shift_8.to_be_taken = True
shift_8.save()
e2.Shifts.add(shift_8)
e2.save()

# Shift 9 for Employee e3
shift_9 = Shift(date=today + datetime.timedelta(days=3), 
                start="11:00am", 
                end="4:00pm")
shift_9.to_be_taken = True
shift_9.save()
e3.Shifts.add(shift_9)
e3.save()

# Shift 10 for Employee e4
shift_10 = Shift(date=today + datetime.timedelta(days=4), 
                 start="8:00am", 
                 end="1:00pm")
shift_10.to_be_taken = True
shift_10.save()
e4.Shifts.add(shift_10)
e4.save()

# Shift 11 for Employee e5
shift_11 = Shift(date=today + datetime.timedelta(days=5), 
                 start="1:00pm", 
                 end="6:00pm")
shift_11.to_be_taken = True
shift_11.save()
e5.Shifts.add(shift_11)
e5.save()

# Shift 12 for Employee e6
shift_12 = Shift(date=today + datetime.timedelta(days=6), 
                 start="2:00pm", 
                 end="7:00pm")
shift_12.to_be_taken = True
shift_12.save()
e6.Shifts.add(shift_12)
e6.save()

# Shift 13 for Employee e7
shift_13 = Shift(date=today + datetime.timedelta(days=7), 
                 start="3:00pm", 
                 end="8:00pm")
shift_13.to_be_taken = True
shift_13.save()
e7.Shifts.add(shift_13)
e7.save()

# Shift 14 for Employee e8
shift_14 = Shift(date=today + datetime.timedelta(days=8), 
                 start="4:00pm", 
                 end="9:00pm")
shift_14.to_be_taken = True
shift_14.save()
e8.Shifts.add(shift_14)
e8.save()

# Shift 15 for Employee e9
shift_15 = Shift(date=today + datetime.timedelta(days=9), 
                 start="5:00pm", 
                 end="10:00pm")
shift_15.to_be_taken = True
shift_15.save()
e9.Shifts.add(shift_15)
e9.save()

# Shift 16 for Employee e10
shift_16 = Shift(date=today + datetime.timedelta(days=10), 
                 start="6:00pm", 
                 end="11:00pm")
shift_16.to_be_taken = True
shift_16.save()
e10.Shifts.add(shift_16)
e10.save()

# Shift for Employee e1
shift_e1 = Shift(date=today + datetime.timedelta(days=1), 
                 start="8:00am", 
                 end="1:00pm")
shift_e1.to_be_taken = True
shift_e1.save()
e1.Shifts.add(shift_e1)
e1.save()

# Shift for Employee e2
shift_e2 = Shift(date=today + datetime.timedelta(days=2), 
                 start="9:00am", 
                 end="2:00pm")
shift_e2.to_be_taken = True
shift_e2.save()
e2.Shifts.add(shift_e2)
e2.save()

# Shift for Employee e3
shift_e3 = Shift(date=today + datetime.timedelta(days=3), 
                 start="10:00am", 
                 end="3:00pm")
shift_e3.to_be_taken = True
shift_e3.save()
e3.Shifts.add(shift_e3)
e3.save()


# Shift for Employee e1
shift_e1 = Shift(date=today, start="7:00am", end="12:00pm")
shift_e1.to_be_taken = True
shift_e1.save()
e1.Shifts.add(shift_e1)
e1.save()

# Shift for Employee e2
shift_e2 = Shift(date=today, start="8:00am", end="1:00pm")
shift_e2.to_be_taken = True
shift_e2.save()
e2.Shifts.add(shift_e2)
e2.save()

# Shift for Employee e3
shift_e3 = Shift(date=today, start="9:00am", end="2:00pm")
shift_e3.to_be_taken = True
shift_e3.save()
e3.Shifts.add(shift_e3)
e3.save()

# Shift for Employee e4
shift_e4 = Shift(date=today, start="10:00am", end="3:00pm")
shift_e4.to_be_taken = True
shift_e4.save()
e4.Shifts.add(shift_e4)
e4.save()

# Shift for Employee e5
shift_e5 = Shift(date=today, start="11:00am", end="4:00pm")
shift_e5.to_be_taken = True
shift_e5.save()
e5.Shifts.add(shift_e5)
e5.save()

# Shift for Employee e6
shift_e6 = Shift(date=today, start="12:00pm", end="5:00pm")
shift_e6.to_be_taken = True
shift_e6.save()
e6.Shifts.add(shift_e6)
e6.save()

# Shift for Employee e7
shift_e7 = Shift(date=today, start="1:00pm", end="6:00pm")
shift_e7.to_be_taken = True
shift_e7.save()
e7.Shifts.add(shift_e7)
e7.save()

# Shift for Employee e8
shift_e8 = Shift(date=today, start="2:00pm", end="7:00pm")
shift_e8.to_be_taken = True
shift_e8.save()
e8.Shifts.add(shift_e8)
e8.save()

# Shift for Employee e9
shift_e9 = Shift(date=today, start="3:00pm", end="8:00pm")
shift_e9.to_be_taken = True
shift_e9.save()
e9.Shifts.add(shift_e9)
e9.save()

# Shift for Employee e10
shift_e10 = Shift(date=today, start="4:00pm", end="9:00pm")
shift_e10.to_be_taken = True
shift_e10.save()
e10.Shifts.add(shift_e10)
e10.save()

# Project 9 - Safety Protocol Update
project9 = Project(project_name="Safety Protocol Update")
project9.save()

# Related Tasks for Project 9
task30 = Task(task_name="Review Current Safety Standards", task_description="Review and assess current safety protocols in the store.", project=project9)
task30.save()
e1.Tasks.add(task30)

task31 = Task(task_name="Develop Safety Training", task_description="Develop a comprehensive safety training program for employees.", project=project9)
task31.save()
e2.Tasks.add(task31)

task32 = Task(task_name="Implement Safety Signage", task_description="Design and implement new safety signage throughout the store.", project=project9)
task32.save()
e3.Tasks.add(task32)

# Project 10 - Customer Experience Enhancement
project10 = Project(project_name="Customer Experience Enhancement")
project10.save()

# Related Tasks for Project 10
task33 = Task(task_name="Gather Customer Feedback", task_description="Collect and analyze customer feedback for improvement.", project=project10)
task33.save()
e4.Tasks.add(task33)

task34 = Task(task_name="Improve In-Store Navigation", task_description="Enhance in-store signage and maps for easier navigation.", project=project10)
task34.save()
e5.Tasks.add(task34)

task35 = Task(task_name="Train Staff in Customer Service", task_description="Provide advanced customer service training to staff.", project=project10)
task35.save()
e6.Tasks.add(task35)

# Project 11 - Eco-Friendly Initiatives
project11 = Project(project_name="Eco-Friendly Initiatives")
project11.save()

# Related Tasks for Project 11
task36 = Task(task_name="Implement Recycling Program", task_description="Set up and promote a recycling program within the store.", project=project11)
task36.save()
e7.Tasks.add(task36)

task37 = Task(task_name="Energy Efficiency Audit", task_description="Conduct an audit to identify ways to improve energy efficiency.", project=project11)
task37.save()
e8.Tasks.add(task37)

task38 = Task(task_name="Source Eco-Friendly Products", task_description="Identify and source eco-friendly products for sale.", project=project11)
task38.save()
e9.Tasks.add(task38)

# Update Task 30
task30.date_created = '2023-12-01 09:00:00'
task30.date_assigned_to = '2023-12-01 10:00:00'
task30.due_date = '2023-12-15'
task30.date_completed = None  # Assuming the task is still in progress
task30.is_complete = False
task30.save()

# Update Task 31
task31.date_created = '2023-12-01 09:30:00'
task31.date_assigned_to = '2023-12-01 10:30:00'
task31.due_date = '2023-12-20'
task31.date_completed = None
task31.is_complete = False
task31.save()

# Update Task 32
task32.date_created = '2023-12-01 10:00:00'
task32.date_assigned_to = '2023-12-01 11:00:00'
task32.due_date = '2023-12-25'
task32.date_completed = None
task32.is_complete = False
task32.save()

# Update Task 33
task33.date_created = '2023-12-02 08:00:00'
task33.date_assigned_to = '2023-12-02 09:00:00'
task33.due_date = '2023-12-16'
task33.date_completed = None
task33.is_complete = False
task33.save()

# Update Task 34
task34.date_created = '2023-12-02 08:30:00'
task34.date_assigned_to = '2023-12-02 09:30:00'
task34.due_date = '2023-12-17'
task34.date_completed = None
task34.is_complete = False
task34.save()

# Update Task 35
task35.date_created = '2023-12-02 09:00:00'
task35.date_assigned_to = '2023-12-02 10:00:00'
task35.due_date = '2023-12-18'
task35.date_completed = None
task35.is_complete = False
task35.save()

# Update Task 36
task36.date_created = '2023-12-03 09:00:00'
task36.date_assigned_to = '2023-12-03 10:00:00'
task36.due_date = '2023-12-19'
task36.date_completed = None
task36.is_complete = False
task36.save()

# Update Task 37
task37.date_created = '2023-12-03 09:30:00'
task37.date_assigned_to = '2023-12-03 10:30:00'
task37.due_date = '2023-12-20'
task37.date_completed = None
task37.is_complete = False
task37.save()

# Update Task 38
task38.date_created = '2023-12-03 10:00:00'
task38.date_assigned_to = '2023-12-03 11:00:00'
task38.due_date = '2023-12-21'
task38.date_completed = None
task38.is_complete = False
task38.save()

# Update Task 24
task24.date_created = '2023-12-01 09:00:00'
task24.date_assigned_to = '2023-12-01 10:00:00'
task24.due_date = '2023-12-05'
task24.date_completed = None  # Assuming the task is still in progress
task24.is_complete = False
task24.save()

# Update Task 25
task25.date_created = '2023-12-01 09:30:00'
task25.date_assigned_to = '2023-12-01 10:30:00'
task25.due_date = '2023-12-06'
task25.date_completed = None
task25.is_complete = False
task25.save()

# Update Task 26
task26.date_created = '2023-12-01 10:00:00'
task26.date_assigned_to = '2023-12-01 11:00:00'
task26.due_date = '2023-12-07'
task26.date_completed = None
task26.is_complete = False
task26.save()

# Update Task 27
task27.date_created = '2023-12-02 09:00:00'
task27.date_assigned_to = '2023-12-02 09:30:00'
task27.due_date = '2023-12-10'
task27.date_completed = None
task27.is_complete = False
task27.save()

# Update Task 28
task28.date_created = '2023-12-02 10:00:00'
task28.date_assigned_to = '2023-12-02 10:30:00'
task28.due_date = '2023-12-11'
task28.date_completed = None
task28.is_complete = False
task28.save()

# Update Task 29
task29.date_created = '2023-12-02 11:00:00'
task29.date_assigned_to = '2023-12-02 11:30:00'
task29.due_date = '2023-12-12'
task29.date_completed = None
task29.is_complete = False
task29.save()
