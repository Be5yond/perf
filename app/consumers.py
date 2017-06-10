from django.http import HttpResponse
from channels.handler import AsgiHandler
from channels import Group
import redis
import json
import time


def http_consumer(message):
    # Make standard HTTP response - access ASGI path attribute directly
    response = HttpResponse("Hello world! You asked for %s" % message.content['path'])
    # Encode that response into message format (ASGI)
    for chunk in AsgiHandler.encode_response(response):
        message.reply_channel.send(chunk)
        

# def ws_message(message):
    # ASGI WebSocket packet-received and send-packet message types
    # both have a "text" key for their textual data.
    # message.reply_channel.send({
    #     "text": message.content['text'],
    # })
    

# Connected to websocket.connect
def ws_add(message):
    # Accept the connection
    message.reply_channel.send({"accept": True})
    # Add to the chat group
    Group("chat").add(message.reply_channel)


# Connected to websocket.receive
def ws_message(message):
    rds = redis.StrictRedis()
    data = json.loads(message.get('text'))
    index, channel = data['index'], data['channel']
    len = rds.llen(channel)
    print index, len
    msg = ''.join(rds.lrange(channel, index, len+1))
    # print msg
    message.reply_channel.send({
        "text":  json.dumps({"msg": msg, "index": len, "channel": channel}),
    })
    if (len-index) < 2:
        time.sleep(10)
    time.sleep(1)


# Connected to websocket.disconnect
def ws_disconnect(message):
    Group("chat").discard(message.reply_channel)
