import requests
import json
import math
from encodings import undefined

# import api key from client-side file
from constants import my_api_read_key

# SGet data from PurpleAir using REST api
# Note: This uses the 10minute PM2.5 average to calculate AQI.
def get_sensor_data(sensor_index):
    # send data request
    my_url = ('https://api.purpleair.com/v1/sensors/' + str(sensor_index))
    my_headers = {'X-API-Key': my_api_read_key}
    response = requests.get(my_url, headers=my_headers)

    # check status codes.
    if response.status_code == 200:
        print('Success!')
    elif response.status_code == 404:
        print('Not Found.')

    # load response as Python object
    pm = json.loads(response.text)['sensor']['stats']['pm2.5_10minute']
    return pm


# USA EPA Formula for AQI
def calc_aqi(cp, ih, il, bph, bpl):
    a = ih - il
    b = bph - bpl
    c = cp - bpl
    return round((a / b) * c + il)

# AQI Calculation using US EPA Qir Quality Breakpoints
def aqi(pm):
    if math.isnan(pm):
        return "-"
    elif pm == 'undefined':
        return "-"
    elif pm < 0:
        return pm
    elif pm > 1000:
        return "-"
    if pm > 350.5:
        return calc_aqi(pm, 500, 401, 500.4, 350.5)  # Hazardous, marron
    elif pm > 250.5:
        return calc_aqi(pm, 400, 301, 350.4, 250.5)  # Hazardous, maroon
    elif pm > 150.5:
        return calc_aqi(pm, 300, 201, 250.4, 150.5)  # Very Unhealthy, purple
    elif pm > 55.5:
        return calc_aqi(pm, 200, 151, 150.4, 55.5)  # Unhealthy, red
    elif pm > 35.5:
        return calc_aqi(pm, 150, 101, 55.4, 35.5)  # Unhealthy for Sensitive Groups, orange
    elif pm > 12.1:
        return calc_aqi(pm, 100, 51, 35.4, 12.1)  # Moderate, yellow
    elif pm >= 0:
        return calc_aqi(pm, 50, 0, 12, 0)  # Good, green
    else:
        return undefined

# logic based on value of aqi
def aqi_ranking():
    if aqi == '-':
        print('The air quality cannot be determined.')
    elif aqi in range(0, 51):
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

# VALUE FOR SELECTED SENSOR STATION
# Enter the desired station number from map.purpleair.com
station = 129299
aqi = aqi(get_sensor_data(station))

# print('The 10-minute average particulate value in George Waiborn Park is: ' + str(pm) + ' ug/m^3')
print('The current air quality index is: ' + str(aqi))
aqi_ranking()

# Next: code to light up WS2812b string running of pizero data pin
# Reminder re: setup https://core-electronics.com.au/guides/ws2812-addressable-leds-raspberry-pi-quickstart-guide/
