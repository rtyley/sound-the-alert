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

GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# this will run in another thread when our events are detected
def octoalert_pressed(channel):
    print("OctoAlert pressed!")
    os.system('omxplayer /home/pi/OctoAlert.AnderDiningRoom.mp3 &')

# raw_input("Press Enter when ready\n>")

def time_needs_sync():
    return 'NTP synchronized: yes' not in subprocess.check_output(['timedatectl', 'status'])

ticks = Observable.interval(100)

def showClock(disp):
    timeText = strftime("%I%M").lstrip("0").rjust(4)
    disp.print_str(timeText)
    disp.set_decimal(1, int(time.time()) % 2)

def showSyncAnim(disp):
    disp.set_decimal(int(time.time()) % 4, True)

clockDisplayStream =  ticks.map(lambda x: showClock)

syncAnimStream = ticks.map(lambda x: showSyncAnim)

truthfulClockStream = Observable.concat(syncAnimStream.take_while(lambda x : time_needs_sync()), clockDisplayStream)

buttonPressSubject = Subject()

GPIO.add_event_detect(26, GPIO.FALLING, callback=buttonPressSubject.on_next, bouncetime=500)

buttonPressSubscription = buttonPressSubject.subscribe(lambda x: octoalert_pressed(x))

display = AlphaNum4.AlphaNum4()
display.begin()
display.set_brightness(0)

displaySubscription = truthfulClockStream.throttle_first(100).subscribe(lambda displayUpdater: renderDisplay(displayUpdater))

def renderDisplay(displayUpdater):
    try:
        display.clear()
        displayUpdater(display)
        display.write_display()
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))

while True:
    time.sleep(1)

GPIO.cleanup()           # clean up GPIO on normal exit
buttonPressSubscription.dispose()
