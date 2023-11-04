from django.contrib import admin
from walrus.models import Employee
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from .models import *

#notifcations

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import HttpResponseRedirect
from django import forms
from django.urls import path
class SendNotificationForm(forms.Form):
    message = forms.CharField(label="Notification Message", max_length=200)

@admin.register(Notifications)

class NotificationAdmin(admin.ModelAdmin):
    add_form_template = "admin/custom_add_form.html"
    
    def add_view(self, request, form_url="", extra_context = None):
        if request.method == "POST":
            form = SendNotificationForm(request.POST)
            if form.is_valid():
                message = form.cleaned_data["message"]

                notification = Notifications.objects.create(message=message)
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    "notifications", {
                        "type": "send_notification",
                        "message": message
                    }
                )

                return HttpResponseRedirect("../{}/".format(notification.pk))
        else:
            form = SendNotificationForm()
        context = self.get_changeform_initial_data(request)
        context["form"]=form
        return super().add_view(request, form_url, extra_context=context)

    def get_urls(self):
        urls = super().get_urls()
        custom_url = [
            path("send-notification/", self.admin_site.admin_view(self.add_view), name="send-notification"),
        ]
        return custom_url + urls

# Register your models here
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Time_Spent)
admin.site.register(Task_Update)
admin.site.register(Shift)


class EmployeeInLine(admin.StackedInline):
    model = Employee
    can_delete = False #can't delete an Employee without deleting the corresponding User
    verbose_name_plural = 'Employee'

class CustomizedUserAdmin(UserAdmin):
    inlines = (EmployeeInLine, )

admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)
admin.site.register(Employee)
