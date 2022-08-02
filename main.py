import requests

# import api key from client-side file
from constants import my_api_read_key
# To use your API key in this file, comment out the line above, and uncomment the line below.
# my_api_read_key = 'YOU API KEY HERE'

# STEP 1: function to send get request to PurpleAir
def getSensorData(sensor_index):
    # my_url is assigned the URL we are going to send our request to.
    my_url = ('https://api.purpleair.com/v1/sensors/' + str(sensor_index))

    # my_headers is assigned the context of our request we want to make. In this case
    # we will pass through our API read key using the variable created above.
    my_headers = {'X-API-Key': my_api_read_key}

    # This line creates and sends the request and then assigns its response to the
    # variable, r.
    response = requests.get(my_url, headers=my_headers)

    # We then return the response we received.
    if response.status_code == 200:
        print('Success!')
    elif response.status_code == 404:
        print('Not Found.')
    print(response.text)
    return response

# STEP 2: function to calculate AQI
# STEP 3: function to control leds

# EXAMPLE:See map for locations https://map.purpleair.com/ and retrieve station # from URLS
getSensorData(129299) #this is the number of the station in George Wainborn Park, Vancouver, BC

