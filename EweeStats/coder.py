#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#

import os
import sys
import shlex
import re
import time
import RPi.GPIO as GPIO

last_encoded = 0
encoder_value = 0

def coder():
    encoder_pin_1 = 23
    encoder_pin_2 = 24
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    temps = 0
    vitesse = 0
    last_encoded = 0
    MSB = 0
    LSB = 0
    circonference = 0.6283

    global encoder_value
    GPIO.add_event_detect(23, GPIO.RISING, callback=update_encoder)
    GPIO.add_event_detect(24, GPIO.RISING, callback=update_encoder)
    temps = time.time()



    while True:
        try:
            compteur = (time.time() - temps)

            if compteur >= 0.25:
                vitesse = 4*encoder_value * 0.22222222*circonference/96
                encoder_value = 0
                temps = time.time()

                print(round(3.6*vitesse, 4))

        except KeyboardInterrupt:
            sys.exit()

def update_encoder(channel):
    global encoder_value
    global last_encoded
    MSB = GPIO.input(23)
    LSB = GPIO.input(24)

    encoded = (MSB << 1) |LSB
    sum = (last_encoded << 2) | encoded

    if (sum == 0b1101 or sum == 0b0100 or sum == 0b0010 or sum == 0b1011):
        encoder_value +=1
    if (sum == 0b1110 or sum == 0b0111 or sum == 0b0001 or sum == 0b1000):
        encoder_value -= 1

    last_encoded = encoded
    return 0


if __name__ == '__main__':
    coder()
