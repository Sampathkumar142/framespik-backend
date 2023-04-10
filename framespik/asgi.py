"""
ASGI config for framespik project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
# from .routing import channel_routing
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path,re_path
from event.consumers  import AlbumConsumer,AudioConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'framespik.settings')


django_asgi = get_asgi_application()


application = ProtocolTypeRouter({
    "http":django_asgi,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                re_path(r'^ws/album/(?P<album_id>\d+)/$', AlbumConsumer.as_asgi()),
                path('ws/voice/<int:album_id>/',AudioConsumer.as_asgi())         ])
        )
    ),
})