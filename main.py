from encodings import undefined
import requests
import json
import math

# import api key from client-side file
from constants import my_api_read_key

# my_api_read_key = 'YOUR API KEY HERE'

# STEP 1: function to send get request to PurpleAir
# Note: the PurpleAir Map uses the 10minute PM2.5 average to calculate AQI, not the point value.


def get_sensor_data(sensor_index):

    # send data request
    my_url = ('https://api.purpleair.com/v1/sensors/' + str(sensor_index))
    my_headers = {'X-API-Key': my_api_read_key}  # PurpleAir prefers the headers method
    response = requests.get(my_url, headers=my_headers)  # response assigned to variable

    # check status codes.
    if response.status_code == 200:
        print('Success!')
    elif response.status_code == 404:
        print('Not Found.')

    # load response as Python object
    response = json.loads(response.text)['sensor']['stats']['pm2.5_10minute']
    return response
    #check if data is valid valueS

# check that pm is a valid reading
def validate_pm(pm):
    if math.isnan(pm):
        return "-"
    elif pm == 'undefined':
        return "-"
    elif pm < 0:
        return pm
    elif (pm > 1000):
        return "-"

# USA EPA Formula for AQI
def calc_aqi(pm, Ih, Il, BPh, BPl):
    a = Ih - Il
    b = BPh - BPl
    c = pm - BPl
    return round((a / b) * c + Il)

# Actual API Calcuation using the USA EPA breakpoint values
def aqi(pm):
    if pm > 350.5:
        return calc_aqi(pm, 500, 401, 500.4, 350.5)  # Hazardous
    elif pm > 250.5:
        return calc_aqi(pm, 400, 301, 350.4, 250.5)  # Hazardous
    elif pm > 150.5:
        return calc_aqi(pm, 300, 201, 250.4, 150.5)  # Very Unhealthy
    elif pm > 55.5:
        return calc_aqi(pm, 200, 151, 150.4, 55.5)  # Unhealthy
    elif pm > 35.5:
        return calc_aqi(pm, 150, 101, 55.4, 35.5)  # Unhealthy for Sensitive Groups
    elif pm > 12.1:
        return calc_aqi(pm, 100, 51, 35.4, 12.1)  # Moderate
    elif pm >= 0:
        return calc_aqi(pm, 50, 0, 12, 0)  # Good
    else:
        return undefined


# SCALE: World Air Quality Index Rating Scale
# air quality scale from WAQI
# 0 - 50 Good (green)
# 51 - 100 Moderate (yellow)
# 101 - 150 Unhealthy for Sensitive Groups (orange)
# 151 - 200 Unhealthy (red)
# 201 - 300 Very Unhealthy (purple)
# 300+ Hazardous (burgundy)

# logic based on value of aqi
def aqi_ranking(aqi):
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

# VALUE FOR SELECTED SENSOR STATION
# Enter the desired station number from map.purpleair.com
pm = get_sensor_data(129299)
aqi= aqi(pm)
print('The 10-minute average particulate value in George Waiborn Park is: ' + str(pm) + ' ug/m^3')
print('The current air quality index is: ' + str(aqi))
report= aqi_ranking(aqi)
