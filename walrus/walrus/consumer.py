
from channels.generic.websocket import AsyncWebsocketConsumer
from django.template import Context, Template
import json
from asgiref.sync import async_to_sync


from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

class NotificationConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):

        user = self.scope['user']
        print("worked")
        if user.is_anonymous:
            # close the connection if the
            # user isn't authenticated yet
            await self.close()
        else:
            #await self.accept()
            #await self.channel_layer.group_add("notifications", self.channel_name)
             # Join group
            await self.channel_layer.group_add(str(user.pk), self.channel_name)
            print(str(user.pk))
            
            await self.accept()
        
        #self.group_name = self.scope['user'].pk
        ## Join group
        #async_to_sync(self.channel_layer.group_add)(
         #   self.group_name,
          #  self.channel_name
       # )
       # self.accept()
        

       

    async def disconnect (self, close_code):
        await self.channel_layer.group_discard("notifications", self.channel_name)
        

    async def send_notification(self, event):
        message = event["message"]


        template = Template('<div class = "notification"><p> {{message}}</p></div>')
        context = Context({"message":message})
        rendered_notification = template.render(context)


        await self.send(
            text_data = json.dumps(
                {
                    "type": "notification",
                    "message":rendered_notification
                }
            )
        )