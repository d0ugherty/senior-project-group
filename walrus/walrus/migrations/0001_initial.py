# Generated by Django 4.2.4 on 2023-11-04 14:53

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_manager', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='No', max_length=6)),
                ('employee_id', models.IntegerField(blank=True, null=True)),
                ('dept', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(null=True)),
                ('start', models.CharField(blank=True, max_length=255, null=True)),
                ('end', models.CharField(blank=True, max_length=255, null=True)),
                ('to_be_taken', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=255)),
                ('task_description', models.CharField(blank=True, max_length=255)),
                ('is_complete', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_assigned_to', models.DateTimeField(blank=True, null=True)),
                ('due_date', models.DateTimeField(blank=True, null=True)),
                ('date_completed', models.DateTimeField(blank=True, null=True)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='walrus.project')),
            ],
        ),
        migrations.CreateModel(
            name='Time_Spent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('in_progress', models.BooleanField(default=False, null=True)),
                ('total_time', models.DurationField(blank=True, default=datetime.timedelta)),
                ('last_clock_in', models.DateTimeField(null=True)),
                ('employee', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='walrus.employee')),
                ('task', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='walrus.task')),
            ],
        ),
        migrations.CreateModel(
            name='Task_Update',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=255)),
                ('venue_image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='walrus.task')),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='Shifts',
            field=models.ManyToManyField(blank=True, null=True, to='walrus.shift'),
        ),
        migrations.AddField(
            model_name='employee',
            name='Tasks',
            field=models.ManyToManyField(blank=True, to='walrus.task'),
        ),
        migrations.AddField(
            model_name='employee',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
