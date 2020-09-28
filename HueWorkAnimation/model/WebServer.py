from flask import Flask
import subprocess

import time
import json
import requests

process_work = None

# Hue wichtige Konstanten (IP, Username, Header, Payload)
bridge_ip = "192.168.178.45"
bridge_username = "J5RVHpoWwgviHQbnYdPaYHJTe63sHIRQxVs1ja6i"
headers = {'content-type': 'application/json'}
# ID der Hueplay
group_id_bars = 4
group_id_lights = 6
# Variable fuer Aktive Konzentrationspausen
work_light = False

# Webserver
model = Flask(__name__)

# Arbeits-Skript
@model.route("/work")
def work():
	global work_light
	global process_work

	work_light = change_bool(work_light)

	if work_light:
		Start_HUE()
		process_work = subprocess.Popen(['python', 'model/HueWorkScript.py'])
		process_av = subprocess.Popen(['python', 'model/AV-Control.py'])

	elif not work_light:
		if process_work:
			process_work.terminate()
		End_HUE()
	return str(work_light)

# Chill-Skript
@model.route("/chill")
def chill():
	global work_light
	global process_work
	global headers

	work_light = False

	if process_work:
		process_work.terminate()

	chill = {"on":True, "bri":250, "xy":[0.48,0.42]}
	r = requests.put("http://"+bridge_ip+"/api/"+bridge_username+"/groups/"+str(group_id_bars)+"/action", data=json.dumps(chill), headers=headers)
	return str(work_light)

# Cozy-Skript
@model.route("/cozy")
def cozy():
	global work_light
	global process_work
	global headers

	work_light = False

	if process_work:
		process_work.terminate()

	cozy_bars = {"on":True, "bri":100, "xy":[0.57,0.35]}
	cozy_lights = {"on":True, "bri":50, "xy":[0.57,0.35]}
	r = requests.put("http://"+bridge_ip+"/api/"+bridge_username+"/groups/"+str(group_id_bars)+"/action", data=json.dumps(cozy_bars), headers=headers)
	r = requests.put("http://"+bridge_ip+"/api/"+bridge_username+"/groups/"+str(group_id_bars)+"/action", data=json.dumps(cozy_lights), headers=headers)
	return str(work_light)

# invertieren eines boolischen Wertes
def change_bool(var):
	return not var

# Feedback beim starten des Arbeitsskriptes
def Start_HUE():
	global headers

	green = {"on":True, "bri": 200, "xy":[0.17,0.7]}
	r = requests.put("http://"+bridge_ip+"/api/"+bridge_username+"/groups/"+str(group_id_bars)+"/action", data=json.dumps(green), headers=headers)
	time.sleep(0.5)

# Feedback beim beenden des Arbeitsskriptes
def End_HUE():
	global headers

	red = {"on":True, "bri": 200, "xy":[0.7,0.3]}
	r = requests.put("http://"+bridge_ip+"/api/"+bridge_username+"/groups/"+str(group_id_bars)+"/action", data=json.dumps(red), headers=headers)
	time.sleep(0.8)
	chill = {"on":True, "bri":250, "xy":[0.48,0.42]}
	r = requests.put("http://"+bridge_ip+"/api/"+bridge_username+"/groups/"+str(group_id_bars)+"/action", data=json.dumps(chill), headers=headers)

# Webserver aufruf
if __name__ == "__main__":
        model.run(host='0.0.0.0',port=1337,debug=False)

