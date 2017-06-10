from channels.routing import route
from .consumers import ws_message, ws_add, ws_disconnect
"""
   module for django channel
"""

channel_routing = [
    # route("http.request", "DemoC.consumers.http_consumer"),
    route("websocket.connect", ws_add),
    route("websocket.receive", ws_message),
    route("websocket.disconnect", ws_disconnect),
]