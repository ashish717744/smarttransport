# geofence function # url # confirm variables of JSON
import json
import time
import requests as r
import RPi.GPIO as GPIO
import math as Math

def geofence():
  # below are the center points of NMIT college
  lat2 = 13.129236
  lon2 =  77.587947
  R = 6371
  centerlat = 13.129056
  centerlon = 77.588292
  dLat = deg2rad(lat2-centerlat)
  dLon = deg2rad(lon2-centerlon)
  a = Math.sin(dLat/2) * Math.sin(dLat/2) + Math.cos(deg2rad(centerlat)) \
    * Math.cos(deg2rad(lat2)) * Math.sin(dLon/2) * Math.sin(dLon/2)
  c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a))
  d = R * c
  return True if d > 1 else False

def deg2rad(deg):
  return deg * (Math.pi/180)


GPIO.setmode(GPIO.BCM)

OnOffRelay = 26
piezobuzzer = 2

GPIO.setup(OnOffRelay, GPIO.OUT)
GPIO.setup(piezobuzzer, GPIO.OUT)

headers = {
    'appKey':"8afb3650-e941-4bd6-894e-6424895813c2",
    'Content-Type':"application/json"
    }

first = True
startTime = time.time()
onoff = "none"

while True:
	if geofence() is False:
		if first:	# if loop is running for the first time outside geofence
			startTime = time.time()	# reassign startTime to start the timer from here
			first = False 	# make it false to not run this code secodn time
		if time.time() - startTime < 120:	# if total time spent is less than 2 minutes
			GPIO.output(piezobuzzer, False)
			time.sleep(1)
			GPIO.output(piezobuzzer, True)
			time.sleep(2)
		else:
			GPIO.output(OnOffRelay, False)		# as the time limit ends
			while onoff == "off":			# if the command from the owner is still 'OFF'
				x = r.get(r"http://192.168.84.250:8080/Thingworx/Things/auto1/Properties/Auto_Status", headers = headers)
				# keep updating # return string in JSON format
				onoff = x.json()['Auto_Status']	# convert that string to JSON
			GPIO.output(OnOffRelay, True)		# Switch on the auto if owner breaks the while loop
			time.sleep(240) 	# give 4 minutes time to the driver to come back inside the geofence

	time.sleep(1)
