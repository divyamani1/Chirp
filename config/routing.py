from django.conf.urls import url

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from notifications.consumers import MyConsumer

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
     # WebSocket chat handler
    "websocket": AuthMiddlewareStack(
        URLRouter([
            url("notifs/$", MyConsumer),
        ])
    ),
})


