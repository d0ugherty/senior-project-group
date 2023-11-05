"""
ASGI config for walrus project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter

from django.core.asgi import get_asgi_application


from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'walrus.settings')

django_application = get_asgi_application()

from . import urls # noqa isort:skip

application = ProtocolTypeRouter(

    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(  AuthMiddlewareStack( URLRouter(urls.websocket_urlpatterns)  )    )
    }

)

#application = get_asgi_application()


