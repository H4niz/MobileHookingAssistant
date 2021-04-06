import time
import frida
import requests
import json

BURP_HOST = 'localhost' 
BURP_PORT = 26080

def my_message_handler(message, payload):
    handled = False
    if message['type'] == 'send':
        body = message['payload']
        if body['from'] == '/http':
            req = requests.request('FRIDA', 'http://%s:%d/' % (BURP_HOST, BURP_PORT), headers={'content-type':'text/plain'}, data=body['payload'])
            # print("----------- PYTHON --------------")
            # # print(req)
            # print(json.loads(req.content))
            script.post({'type': 'x', 'payload': json.loads(req.content)})

            handled = True

    # if not handled:
    #     my_message_handler(message, payload)


device = frida.get_usb_device()
pid = device.spawn(["com.vietinbank.ipay"])
device.resume(pid)
time.sleep(1) 
session = device.attach(pid)
with open("test_ob.js", encoding='utf8') as f:
    script = session.create_script(f.read())
script.on("message", my_message_handler)
script.load()
time.sleep(1)
input()