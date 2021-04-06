import frida
import requests

BURP_HOST = "localhost"
BURP_PORT = 26080

def frida_process_message(self, message, data, ui):
    handled = False

    if message['type'] == 'input':
        handled = True
    elif message['type'] == 'send':
        stanza = message['payload']

        if stanza['from'] == '/http':
            req = requests.request('FRIDA', 'http://%s:%d/' % (BURP_HOST, BURP_PORT), headers={'content-type':'text/plain'}, data=stanza['payload'])
            self._script.post({ 'type': 'input', 'payload': req.content })
            handled = True

    if not handled:
        frida_process_message(message, data, ui)

tracer.Tracer.__process_message = tracer.Tracer._process_message
tracer.Tracer._process_message = frida_process_message

if __name__ == '__main__':
    print("[x] To intercept in Burp, set up an invisible proxy listening on port %d, forwarding to the echo server." % BURP_PORT)
    tracer.main()