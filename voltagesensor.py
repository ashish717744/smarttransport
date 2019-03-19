import requests as r
import Adafruit_MCP3008
import time

CLK = 18
MISO = 23
MOSI = 24
CS = 25

mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

while True:
	onoff = '{"onoff" : "on"}' if mcp.read_adc(3) else '{"onoff" : "off"}'
	lights = '{"lights" : "on"}' if mcp.read_adc(4) else '{"lights" : "off"}'
	wiper = '{"wiper" : "on"}' if mcp.read_adc(5) else '{"wiper" : "off"}'

	r.put('http://192.168.84.250:8080/Thingworx/Things/auto1/Properties/Auto_Status', param = onoff)
	r.put('http://192.168.84.250:8080/Thingworx/Things/auto1/Properties/Head_Light', param = lights)
	r.put('http://192.168.84.250:8080/Thingworx/Things/auto1/Properties/Wiper', param = wiper)
