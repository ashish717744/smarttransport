import RPi.GPIO as GPIO
import Adafruit_MCP3008
import time
import json
import requests as r

GPIO.setmode(GPIO.BCM)

wiperRelay = 15
switch = 3

CLK = 18
MISO = 23
MOSI = 24
CS = 25

GPIO.setup(wiperRelay, GPIO.OUT)
headers = {
    'appKey':"8afb3650-e941-4bd6-894e-6424895813c2",
    'Content-Type':"application/json"
    }

mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# if auto is in manual mode then it'll be detected by another python file
# sent to thingWorx and then thingWorx will make the owner control value false
while True:
	owner = r.get(r"http://192.168.84.250:8080/Thingworx/Things/auto1/Properties/Wiper",headers = headers)
	owner = owner.json()
	if owner['mode']:		# for owner control
		GPIO.output(wiperRelay, True) if owner['Wiper'] else GPIO.output(wiperRelay, False)
	else: 					# for sensor control
		# Rain sensor analog value ranges from 200 to 1000 and the threshold is decided to be 650
		# When there is rain drop on the rain sensor then less value is shown
		rainIntensity = mcp.read_adc(1)		#read from pin 1 of ADC
		if rainIntensity > 200:
			# delay = 0 if 'rainIntensity > MID' else 3 # bracket is executed if 'rainIntensity < 500' else 5
			# syntax of ternary statement in python < 'first' if True else 'second' />
			delay = (0 if rainIntensity < 350 else 3) if rainIntensity < 500 else 5
			GPIO.output(wiperRelay, True)
			time.sleep(0.5)
			while GPIO.input(switch) is False:
				GPIO.output(wiperRelay, True)
			GPIO.output(wiperRelay, False)
			time.sleep(delay)		# calculated rest for wiper after every cycle according to the intensity
		else:
			GPIO.output(wiperRelay, False)
	time.sleep(0.5)
