# Python program to find current
# weather details of any city
# using openweathermap api

# import required modules
import requests, json
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import time
import pymysql.cursors
import mysql.connector
from mysql.connector import Error


from datetime import datetime
channel = 21


def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(query)
        print(f"Error: '{err}'")


# Enter your API key here
api_key = "ENTER_API_KEY" #https://openweathermap.org/api

# base_url variable to store url
base_url = "http://api.openweathermap.org/data/2.5/weather?"

# Give city name
city_name = "Paris"

# complete_url variable to store
# complete url address
complete_url = base_url + "appid=" + api_key + "&q=" + city_name + "&units=metric"


while True:
    # get method of requests module
    # return response object
    response = requests.get(complete_url)

    # json method of response object
    # convert json format data into
    # python format data
    x = response.json()

    # Now x contains list of nested dictionaries
    # Check the value of "cod" key is equal to
    # "404", means city is found otherwise,
    # city is not found
    if x["cod"] != "404":

        # store the value of "main"
        # key in variable mainInfo
        mainInfo = x['main']

        # store the value corresponding
        # to the "temp" key of mainInfo
        current_temperature = mainInfo["temp"]
        current_Hightemperature = mainInfo["temp_max"]
        current_Lowtemperature = mainInfo["temp_min"]

        # store the value corresponding
        # to the "pressure" key of mainInfo
        current_pressure = mainInfo["pressure"]

        # store the value corresponding
        # to the "humidity" key of mainInfo
        current_humidity = mainInfo["humidity"]

        # store the value corresponding
        # to the "wind speed" key of mainInfo
        current_windSpeed = mainInfo["humidity"]

        # store the value of "wind"
        # key in variable windInfo
        windInfo = x["wind"]

        # store the value corresponding
        # to the "speed" key of windInfo
        wind_speed = windInfo["speed"]

        # store the value corresponding
        # to the "speed" key of windInfo
        wind_degree = windInfo["deg"]

        # store the value of "wind"
        # key in variable windInfo
        otherInfo = x["sys"]

        # store the value corresponding
        # to the "sunrise" key of otherInfo
        sunrise_time = otherInfo["sunrise"]

        # store the value corresponding
        # to the "sunset" key of otherInfo
        sunset_time = otherInfo["sunset"]

        # store the value of "weather"
        # key in variable weatherInfo
        weatherInfo = x["weather"]

        # store the value corresponding
        # to the "description" key at
        # the 0th index of weatherInfo
        weather_description = weatherInfo[0]["description"]
 
        sqlquery = """
                    INSERT INTO Home_Automation (field, value) VALUES 
                    ('weather_temperature', {0}),
                    ('weather_max_temperature', {1}),
                    ('weather_min_temperature', {2}),
                    ('weather_atmospheric_pressure', {3}),
                    ('weather_humidity', {4}),
                    ('weather_wind_speed', {5}),
                    ('weather_wind_degree', {6}),
                    ('weather_sunrise_time', {7}),
                    ('weather_sunset_time', {8});
                   """
        sqlquery2 = """
                    INSERT INTO Home_Automation (field, field_char) VALUES 
                    ('weather_description', '{0}')
                    """

        connection = create_db_connection("localhost", "root", "pv", "IoT_Project")
        execute_query(connection, sqlquery.format(str(current_temperature), str(current_Hightemperature), str(current_Lowtemperature),
                                                  str(current_pressure),  str(current_humidity), str(wind_speed), str(wind_degree),
                                                  str(sunrise_time), str(sunset_time)))
        
        execute_query(connection, sqlquery2.format(weather_description))
        if (float(str(current_temperature)) >= 20):
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(channel, GPIO.OUT)
            GPIO.output(channel, GPIO.HIGH)
            time.sleep(1800)
            GPIO.output(channel, GPIO.LOW)
            time.sleep(0.1)
            GPIO.cleanup()
                      
        publishString = (" Temperature (in celsius unit) = " +
                        str(current_temperature) +
              "\n Max Temperature (in celsius unit) = " +
                        str(current_Hightemperature) +
              "\n Min Temperature (in celsius unit) = " +
                        str(current_Lowtemperature) +
              "\n Atmospheric Pressure (in hPa unit) = " +
                        str(current_pressure) +
              "\n Humidity (in percentage) = " +
                        str(current_humidity) +
              "\n Wind Speed (in m/s unit) = " +
                        str(wind_speed) +
              "\n Wind Degree (in degrees) = " +
                        str(wind_degree) +
              "\n Sunrise Time (in unix) = " +
                        str(sunrise_time) +
              "\n Sunset Time (in unix = " +
                        str(sunset_time) +
              "\n description = " +
                        str(weather_description))
        
        print(publishString)

