##### subscriber script ####
import RPi.GPIO as GPIO
import time # for time function
import paho.mqtt.client as mqtt
import pymysql.cursors 

broker = "IP ADDRESS OF RASPBERRY PI"
channel = 21


def on_connect(client , userdata, flags, rc): # what to do when we connect to the broker]
    if (rc==0):
        client.subscribe("IRdata")
        print ("Subscribed to IRdata")
    else :
        client.reconnect()

def on_message(client, userdata, msg):
    print (msg.payload.decode("utf-8"))
    if (msg.payload.decode("utf-8") == "Obstacle"):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(channel, GPIO.OUT)
        GPIO.output(channel, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(channel, GPIO.LOW)
        time.sleep(0.1)
        GPIO.cleanup()
    connect(msg)

def connect(msg):
    connection = pymysql.connect(
      user='root',
      password='pv',
      host='localhost',
      database='IoT_Project',
      cursorclass=pymysql.cursors.DictCursor
    )
    with connection:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `IR` (`field`,`value`) VALUES (%s, %s)"
            cursor.execute(sql, (msg.topic, msg.payload.decode("utf-8")))
        connection.commit()

client = mqtt.Client("IRdata",protocol=mqtt.MQTTv31)
client.on_connect = on_connect # this will call the on_connect function
client.on_message = on_message # this will call the on_message function
client.connect(broker, 1883, 60) # broker connection
client.loop_forever()


