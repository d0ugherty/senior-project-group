from csv import DictReader
from datetime import datetime

from django.core.management import BaseCommand
from pytz import UTC
from walrus.models import Tasks


DATETIME_FORMAT = '%m/%d/%Y %H:%M'

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the Event data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from task.csv into our Task model"

    def handle(self, *args, **options):
        if Tasks.objects.exists():
            print('Task data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
        print("Loading event data for events available for adoption")
        for row in DictReader(open('./task.csv')):
            task = Tasks()
            task_name = row['task_name']
            task_description = row['task_description']
            is_complete = row['is_complete']
            updates = row['updates']
            raw_submission_date_1 = row['date_created']
            submission_date = UTC.localize(
                datetime.strptime(raw_submission_date_1, DATETIME_FORMAT))
            task.date_created = submission_date
            raw_submission_date_2 = row['date_assigned']
            submission_date_2 = UTC.localize(
                datetime.strptime(raw_submission_date_2, DATETIME_FORMAT))
            task.date_assigned = submission_date_2
            raw_submission_date_3 = row['due_date']
            submission_date_3 = UTC.localize(
                datetime.strptime(raw_submission_date_3, DATETIME_FORMAT))
            task.due_date = submission_date_3
            date_assigned = row['date_assigned']
            due_date = row['due_date']
            project_id = row['project_id']
            task.save()