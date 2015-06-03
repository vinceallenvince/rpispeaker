import RPi.GPIO as GPIO
import time
from urllib2 import Request, urlopen, URLError
import json
from subprocess import call

GPIO.setmode(GPIO.BCM)

ready = False
base_client_uri = "http://127.0.0.1:15004"

###################

LED = 23
LED_count = 0
LED_state = 1
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, True)

def led_on():
    GPIO.output(LED, True)

def led_off():
    GPIO.output(LED, False)

###################

button_shutdown = 5
GPIO.setup(button_shutdown, GPIO.IN, pull_up_down=GPIO.PUD_UP)

###################

def play():
    global playing
    playing = True
    req = Request(base_client_uri + "/action?action=play")
    urlopen(req)

def play_preset1():
    global playing
    playing = True
    req = Request(base_client_uri + "/action?action=preset-1")
    urlopen(req)

def pause():
    global playing
    playing = True
    req = Request(base_client_uri + "/action?action=pause")
    urlopen(req)

def set_max_connect_volume():
    req = Request(base_client_uri + "/action?action=volume&level=65535")
    urlopen(req)

def shutdown_pi():
    call(["/home/pi/shutdown.sh"])

def check_ready():
    global ready, LED_count, LED_state, Request, URLError
    if ready == False :
        req = Request(base_client_uri + "/status-data")
        try:
            response = urlopen(req)
        except URLError as e:
            if hasattr(e, "reason"):
                LED_count += 1
                if LED_count > 40:
                    LED_state *= -1
                    LED_count = 0
                if LED_state == 1:
                    led_on()
                else:
                    led_off()
                #print 'We failed to reach a server.'
                #print 'Reason: ', e.reason
            elif hasattr(e, "code"):
                #print 'The server couldn\'t fulfill the request.'
                #print 'Error code: ', e.code
                pass
        else:
            # everything is fine
            ready = True
            led_on()
            set_max_connect_volume() # max the Spotify connect volume
            #set_volume(y)
            play_preset1()

while True:
    if ready == True :
        shutdown_state = GPIO.input(button_shutdown)
        if shutdown_state == False:
            print("shutdown button Pressed")
            shutdown_pi()
            time.sleep(0.2)

    else:
        check_ready()
