#!/usr/bin/env python2.7
# See also http://RasPi.tv/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio-part-3
from __future__ import print_function

import os
import subprocess

import RPi.GPIO as GPIO
from rx.subjects import Subject
from rx import Observable, Observer

import time
from time import strftime
from Adafruit_LED_Backpack import AlphaNum4
import os.path

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

ticks = Observable.interval(100)

def showClock(disp):
    timeText = strftime("%H%M")
    disp.print_str(timeText)
    disp.set_decimal(1, int(time.time()) % 2)

def showSyncAnim(disp):
    disp.set_decimal(int(time.time()) % 4, True)

clockDisplayStream =  ticks.map(lambda x: showClock)

syncAnimStream = ticks.map(lambda x: showSyncAnim)

truthfulClockStream = Observable.concat(syncAnimStream.take_while(lambda x : time_needs_sync()), clockDisplayStream)

buttonPressSubject = Subject()

GPIO.add_event_detect(25, GPIO.FALLING, callback=buttonPressSubject.on_next, bouncetime=500)

buttonPressSubscription = buttonPressSubject.subscribe(lambda x: octoalert_pressed(x))

display = AlphaNum4.AlphaNum4()

display.begin()

displaySubscription = truthfulClockStream.throttle_first(100).subscribe(lambda displayUpdater: renderDisplay(displayUpdater))

def renderDisplay(displayUpdater):
    display.clear()
    displayUpdater(display)
    display.write_display()

while True:
    time.sleep(1)

GPIO.cleanup()           # clean up GPIO on normal exit
buttonPressSubscription.dispose()
