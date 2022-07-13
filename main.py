# Air Quality Lamp
# A personal project

# data from http://waqi.info/
# description: a python script to check the local air quality index (AQI) and set the colour of a string of WS2812B LEDs

# Helpful resources:
# https://www.w3schools.com/python/python_json.asp
# https://www.w3schools.com/python/module_requests.asp
# https://www.w3schools.com/python/python_dictionaries.asp
# https://www.programiz.com/python-programming/nested-dictionary
# https://www.askpython.com/python/examples/pull-data-from-an-api
# https://oxylabs.io/blog/python-parse-json
# https://aqicn.org/json-api/doc/#api-Geolocalized_Feed-GetHereFeed
# https://restfulapi.net/


# import modules
import requests
import json

# import API url and key
import constants

# Get Data
response = requests.get(constants.API_url)  # connect to api url and get response object
resp_json = json.loads(response.text)  # loads json response object as a Python dictionary
# print(type(resp_json)) #uncomment to check type
aqi = resp_json['data']['aqi']  # return key value for air quality index (aqi)
print('The current Air Quality Index is:', aqi)  # print aqi

# SCALE: World Air Quality Index Rating Scale
# air quality scale from WAQI
# 0 - 50 Good (green)
# 51 - 100 Moderate (yellow)
# 101 - 150 Unhealthy for Sensitive Groups (orange)
# 151 - 200 Unhealthy (red)
# 201 - 300 Very Unhealthy (purple)
# 300+ Hazardous (burgundy)

# logic based on value of aqi
if aqi in range(0, 51):
    print('The air quality is good.')
elif aqi in range(51, 101):
    print('The air quality is moderate.')
elif aqi in range(101, 150):
    print('The air quality is unhealthy for sensitive groups.')
elif aqi in range(151, 200):
    print('The air quality is unhealthy.')
elif aqi in range(200, 301):
    print('The air quality is very unhealthy.')
else:
    print('The air quality is hazardous.')
# Next: code to light up WS2812b string running of pizero data pin
# Reminder re: setup https://core-electronics.com.au/guides/ws2812-addressable-leds-raspberry-pi-quickstart-guide/