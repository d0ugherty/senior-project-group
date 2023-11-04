"""walrus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

from django.conf import settings
from django.conf.urls.static import static

from walrus import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", views.home_redirect, name="home"),
    path('list_tasks/', views.list_tasks, name='list_tasks'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('add_task/', views.add_task, name='add_task'),
    path('delete_task/<int:task_id>', views.delete_task, name='delete_task'),
    path('manager_home/', views.load_manager_home, name='manager_home'),
    path('manager_home/manager_home_redirect', views.manager_home_redirect, name='manager_home_redirect'),
    path('employee_stats/', views.employee_stats, name='employee_stats'),
    path('home/<int:employee_id>/', views.home_page, name='home_page'),
    #path('employee_stats/<int:employee_id>', views.get_stats, name="get_stats")
    path('update_task_status/<int:task_id>',views.update_task_status, name='update_task_status'),
    path('manager_home/edit_task/<int:task_id>', views.edit_task, name='edit_task'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
