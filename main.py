#!/usr/bin/env python2.7
# See also http://RasPi.tv/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio-part-3
from __future__ import print_function

import os
import subprocess

import RPi.GPIO as GPIO
from rx.subjects import Subject

GPIO.setmode(GPIO.BCM)

# GPIO 23 set up as inputs, pulled up to avoid false detection.
# Both ports are wired to connect to GND on button press.
# Ie button press will connect GPIO port 25 to GND
# So we'll be setting up falling edge detection
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# this will run in another thread when our events are detected
def octoalert_pressed(channel):
    print("OctoAlert pressed!")
    os.system('omxplayer /home/pi/OctoAlert.AnderDiningRoom.mp3 &')

# raw_input("Press Enter when ready\n>")

def time_needs_sync():
    return subprocess.check_output(['ntpq', '-c', 'rv 0 reftime']).startswith('reftime=0000')

buttonPressSubject = Subject()

GPIO.add_event_detect(25, GPIO.FALLING, callback=buttonPressSubject.on_next, bouncetime=500)

buttonPressSubscription = buttonPressSubject.subscribe(lambda x: octoalert_pressed)

import time
from time import strftime
from Adafruit_LED_Backpack import AlphaNum4
import os.path

display = AlphaNum4.AlphaNum4()

display.begin()

pos = 0

while True:
    display.clear()
    display.set_brightness(0)

    timeText = strftime("%H%M")

    if time_needs_sync():
        display.set_decimal(pos % 4, True)
    else:
        display.print_str(timeText)
        display.set_decimal(1, pos % 2)

    display.write_display()

    pos += 1
    time.sleep(1)

GPIO.cleanup()           # clean up GPIO on normal exit
buttonPressSubscription.dispose()
