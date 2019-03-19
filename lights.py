
# tell software team about new variables # check luminousity in street lights
import json
import requests as r
import RPi.GPIO as GPIO
import Adafruit_MCP3008
import time

GPIO.setmode(GPIO.BCM)

lightRelay = 14
CLK = 18
MISO = 23
MOSI = 24
CS = 25

GPIO.setup(lightRelay, GPIO.OUT)

headers = {
    'appKey':"8afb3650-e941-4bd6-894e-6424895813c2",
    'Content-Type':"application/json"
    }

mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)
luminousityLimit = 600

# if auto is in manual mode then it'll be detected by another python file
# sent to thingWorx and then thingWorx will make the owner control value false
while True:
	owner = r.get(r"http://192.168.84.250:8080/Thingworx/Things/auto1/Properties/Head_Light", headers = headers)
	owner = owner.json()
	if owner['mode']:		# for owner control
		GPIO.output(lightRelay, True) if owner['Head_Light'] else GPIO.output(lightRelay, False)
	else:				# for sensor control
		luminousity = mcp.read_adc(0)
		if luminousity > luminousityLimit:
			time.sleep(0.5)			# this delay makes sure that the luminousity is constant of 0.5 seconds
			if luminousity > luminousityLimit:
				GPIO.output(lightRelay, True)
		else:
			time.sleep(2)			# this delay makes sure that the luminousity is constant of 2 seconds
			if luminousity < luminousityLimit:
				GPIO.output(lightRelay, False)
	time.sleep(0.5)
