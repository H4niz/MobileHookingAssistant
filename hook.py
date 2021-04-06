import time
import frida
import requests

PACKAGE_NAME = ""
PATH_2_SCRIPT = ""

def my_message_handler(message, payload):
    if message['type'] == 'send':
        print(message['payload'])

device = frida.get_usb_device()
pid = device.spawn([PACKAGE_NAME])
device.resume(pid)
time.sleep(1) 
session = device.attach(pid)
with open(PATH_2_SCRIPT) as f:
    script = session.create_script(f.read())
script.on("message", my_message_handler)
script.load()
time.sleep(1)
input()
