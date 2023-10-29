# Generated by Django 4.2.4 on 2023-10-29 01:44

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('walrus', '0003_task_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateField(blank=True, default=datetime.date(2023, 10, 28)),
        ),
        migrations.AlterField(
            model_name='task',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='walrus.project'),
        ),
        migrations.CreateModel(
            name='Time_Spent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='walrus.employee')),
                ('task', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='walrus.task')),
            ],
        ),
    ]
