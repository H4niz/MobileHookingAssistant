#!"C:\Program Files\Python37\python3.exe"
# -*- coding: utf-8 -*-

import sys, time
import frida
import base64
from goto import with_goto
import threading, subprocess
import requests
import json, array

PROC_ID = 0
PACKAGGE_NAME = ""
BURP_HOST = 'localhost' 
BURP_PORT = 26080

BG_HOOK = ".//functions//bg_hook.js"
ENUM_MODULE = ".//functions//enum_module.js"
ENUM_CLASSES = ".//functions//enum_classes.js"
ENUM_MOTHODS = ".//functions//enum_methods.js"
GET_ANDROIDID = ".//functions//get_androidid.js"
ENUM_NATIVE_FUNC = ".//functions//enum_nativecfunctions.js"
ENUM_ALL = ".//functions//enum_all.js"
HOOKING_STRING = ".//functions//hooking_string.js"
CUSTOM_HOOK = ".//functions//custom_hook.js"
TRACING_API = ".//burp_invisible_prosy//api_handler.js"

global script, processid, process_name


class colors: 
    reset='\033[0m'
    bold='\033[01m'
    disable='\033[02m'
    underline='\033[04m'
    reverse='\033[07m'
    strikethrough='\033[09m'
    invisible='\033[08m'
    class bg: 
        black='\033[40m'
        red='\033[41m'
        green='\033[42m'
        orange='\033[43m'
        blue='\033[44m'
        purple='\033[45m'
        cyan='\033[46m'
        lightgrey='\033[47m'
    class fg: 
        black='\033[30m'
        red='\033[31m'
        green='\033[32m'
        orange='\033[33m'
        blue='\033[34m'
        purple='\033[35m'
        cyan='\033[36m'
        lightgrey='\033[37m'
        darkgrey='\033[90m'
        lightred='\033[91m'
        lightgreen='\033[92m'
        yellow='\033[93m'
        lightblue='\033[94m'
        pink='\033[95m'
        lightcyan='\033[96m'

class log:
	def info(self, msg):
		print("{}[INFO] - {}{}".format(colors.bg.blue, msg, colors.reset))
		return 
	def fg_info(self, msg):
		print("{}[INFO] - {}{}".format(colors.fg.blue, msg, colors.reset))
		return 
	def warning(self, msg):
		print("{}[WARNING] - {}{}".format(colors.bg.orange, msg, colors.reset))
		return  
	def fg_warning(self, msg):
		print("{}[WARNING] - {}{}".format(colors.fg.orange, msg, colors.reset))
		return 
	def failure(self, msg):
		print("{}[FAILURE] - {}{}".format(colors.bg.red, msg, colors.reset))
		return  
	def fg_failure(self, msg):
		print("{}[FAILURE] - {}{}".format(colors.fg.red, msg, colors.reset))
		return 
	def success(self, msg):
		print("{}[SUCCESS] - {}{}".format(colors.bg.green, msg, colors.reset))
		return  
	def fg_success(self, msg):
		print("{}[SUCCESS] - {}{}".format(colors.fg.green, msg, colors.reset))
		return 
	def show(self, msg):
		print("{}".format(msg))
		return 

def on_message(message, data):
	if message['type'] == 'send':
		if 'from' in message['payload'].keys():
			body = message['payload']
			req = requests.request('FRIDA', 'http://%s:%d/' % (BURP_HOST, BURP_PORT), headers={'content-type':'text/plain'}, data=body['payload'])
			print(req.content)
			try:
				# data = json.loads(req.content)
				data = json.loads(req.content)
				# print("[Python] - Data type: {}".format(type(data)))
			except Exception as e:
				log.fg_failure(e)
				pass

			global script
			script.post({'type': 'x', 'payload': data})

		else:
			with open("./outputs/" + str(message['payload']['filename']), "a+", encoding='utf8') as f:
				if( message['payload']['isencode'] == "True"):
					f.write( message['payload']['data'] + "=Base64=>" + str(base64.b64encode(message['payload']['data'].encode())))
					f.write(str("\n"))
				else:
					f.write( message['payload']['data'])
					f.write(str("\n"))
	return

def load_function(session, SCRIPT_NAME):
	try:
		log.show("Loading script...")
		script = session.create_script(open(SCRIPT_NAME, "r", encoding='utf-8').read().strip())
		log.success("Load script {} successful!".format(SCRIPT_NAME))
		return script
	except Exception as e:
		log.failure(e)
	return

	return script

def type_of_hook():
	log.show("Which types?")
	log.show("\t1. Attach")
	log.show("\t2. Spawn")
	choice = int(input("> "))
	if(choice == 1):
		obj = int(input("PID to Attach> "))
		global processid
		processid = obj
	else:
		obj = str(input("Package name> "))
		global process_name
		process_name = obj

	return choice

def make_script(wrapper, func, params):
	samples = """
		console.log("Custom hooking...");
		Java.perform(function x(){ 
		"""    
	samples +=    	'var my_class = Java.use("{}");'.format(wrapper)
	samples +=		'my_class.{}.implementation = function({}){'.format(func, params)
	samples += """
	    var ret_value = this.fun(2,5);
	    return ret_value; 
    }});
	"""
	return samples

def device_info(device, processid):
	log.show("{}\t\t\t Device Info \t\t\t{}".format(colors.bg.blue, colors.reset))
	log.show("Device: {}\nEmulator: {}".format(device.id, device.name))
	log.show("{}\t\t\t Device Info \t\t\t{}".format(colors.bg.blue, colors.reset))
	print("\n")
	log.show("{}\t\t\t Process Info \t\t\t{}".format(colors.bg.blue, colors.reset))
	log.show("Process ID: {}".format(processid))
	proc_enum = device.enumerate_processes()
	for proc in proc_enum:
		if( len(proc.name) >= 10 ):
			log.show("{} - {}".format(proc.pid, proc.name))
	log.show("{}\t\t\t Process Info \t\t\t{}".format(colors.bg.blue, colors.reset))

	print("\n")
	return

def hook(choice):
	i = 0
	global process_name, processid
	while i < 5:
		try:
			if choice == 1:
				session = frida.attach(processid)
				log.success("Process ID: {}".format(processid))
				return session
			elif choice == 2:
				device = frida.get_usb_device(timeout=5)
				# device = frida.get_device('192.168.81.102:5555')
				log.success("Device: {}".format(device))
				# device = frida.get_remote_device()
				pid = device.spawn([process_name])
				log.success("Spawn Process successful!")
				log.fg_success("Hooking package: {}".format(process_name))
				device_info(device, pid)

				time.sleep(0.1)
				session = device.attach(pid)
				device.resume(pid)
				return session
			else:
				log.failure("Can not find PID/Package")
				return
		except Exception as e:
			log.failure(e)
			i+=1
		log.info("Try again. {} time(s)".format(i))

	sys.exit(1)

def author():
	log.show("{}\t\t\t AnhNLQ a.k.a h4niz\t\t\t{}".format(colors.bg.red, colors.reset))
	return 

def menu():
	global process_name
	log.fg_success("Current hooking: {}".format(process_name))
	log.info("\t======= SELECTION =========")
	log.show("\t0. Show running thread")
	log.show("\t1. Enumerate modules")
	log.show("\t2. Enumerate classes")
	log.show("\t3. Enumerate methods")
	log.show("\t4. Enumerate Native C/C++ Functions")
	log.show("\t5. Hooking StringBuilder/StringBuffer")
	log.show("\t6. Tracing API")
	log.show("\t7. Custom Script")
	log.show("\t8. Custom Hook")
	log.show("\t9. Reload app")

	log.show("\t10. Exit")
	choice = int(input("> "))
	return choice

def load_script(_script):
	log.info("Create new thread...")
	_script.on('message', on_message)
	_script.load()
	global script
	script = _script
	return 

def info_trace_api():
	log.info("======== API TRACE REQUIRED =========")
	log.show("1. Setup burpsuit to listen at: localhost:26080 and redirect to: localhost:27080")
	log.show("2. Insert the script below into your javascript code:")
	log.fg_warning("		send({from: '/http', payload: data})")
	log.fg_warning("		var modify_data = \"None\";")
	log.fg_warning("		var op = recv('x', function(x) {")
	log.fg_warning("			modify_data = JSON.stringify(x.payload);")
	log.fg_warning("		});")
	log.fg_warning("		op.wait();")
	log.show("3. Give me script hook name")
	script_hook = r'C:\Users\cloud\OneDrive - HPTVietnam Corporation\Frida\functions\trace_api.js'
	log.info("======== API TRACE REQUIRED =========")
	# ready = input("Are you ready?(y/n)")
	# if ready == 'n' or ready == 'N':
	# 	return None
	return script_hook

def run_echo_server():
	# r = subprocess.run(['python', './burp_invisible_prosy/echo-server.py'], capture_output=True)
	exec('./burp_invisible_prosy/echo-server.py')
	return 

def enum_thread():
	for x in threading.enumerate():
		log.show(x)
	return 

@with_goto
def main(choice):
	label .begin
	author()
	list_threads = list()

	ss = hook(choice)
	flag = list()
	label .menu
	global script
	script	= load_function(ss, BG_HOOK	)
	load_thread = threading.Thread(target=load_script, args=(script,))
	load_thread.daemon = True
	list_threads.append(load_thread)
	load_thread.start()
	
	while(True):
		c = menu()
		if(c == 0 and c not in flag):
			enum_thread()
			flag.append(0)
			goto .menu
		if(c == 1 and c not in flag):
			script = load_function(ss, ENUM_MODULE)
			flag.append(1)
		elif (c == 2 and c not in flag):
			script = load_function(ss, ENUM_CLASSES)
			flag.append(2)
		elif (c == 3 and c not in flag):
			script = load_function(ss, ENUM_MOTHODS)
			flag.append(3)
		elif (c == 4 and c not in flag):
			script = load_function(ss, ENUM_NATIVE_FUNC)
			flag.append(4)
		elif (c == 5 and c not in flag):
			script = load_function(ss, HOOKING_STRING)
			flag.append(5)
		elif (c == 6 and c not in flag):
			# script = load_function(ss, TRACING_API)
			# run_echo_server = threading.Thread(target=run_echo_server)
			# run_echo_server.daemon = True
			script_hook = info_trace_api()
			if script_hook is None:
				goto .menu
			script = load_function(ss, script_hook)
			from echo_server import main as echo_main
			echo_thread = threading.Thread(target=echo_main)
			echo_thread.daemon = True
			list_threads.append(echo_thread)
			echo_thread.start()
			log.warning("Running Burp with listening on port 26080 then redirect to 27080")
			flag.append(6)
		elif (c == 7 and c not in flag):
			CUSTOM_SCRIPT = "./functions/custom_script.js"	
			script = load_function(ss, CUSTOM_SCRIPT)
			flag.append(7)
		elif (c == 8 and c not in flag):
			script = load_function(ss, CUSTOM_HOOK)
			flag.append(8)
		elif (c == 9):
			goto .begin
		elif (c == 10):
			ss.detach()
			sys.exit(1)

		# list_threads.append(load_thread)
		# load_thread.start()

	
if __name__ == '__main__':
	log = log()
	global processid, process_name

	processid = PROC_ID 
	process_name = PACKAGGE_NAME 

	if processid != 0:
		choice = 1
	elif process_name is not None:
		choice = 2

	elif processid != 0 and process_name is not None:
		choice = 2
	else :
		choice = type_of_hook()
	

	main(choice)
