import frida, sys, time

def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)
    script.post({"type":"x", "payload":"Data from Python.."})


jscode = """
Java.perform(function () {
  var data_to_send = "Data from JS";
  var data_to_recv = "";

  send(data_to_send);
  var r = recv("x", function(x) {console.log(x.payload);}).wait();
});
"""

device = frida.get_usb_device()
pid = device.spawn(["com.android.insecurebankv2"])
device.resume(pid)
time.sleep(1) 
session = device.attach(pid)
script = session.create_script(jscode)
script.on('message', on_message)
script.load()

sys.stdin.read()