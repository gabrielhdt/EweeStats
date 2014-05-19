# -*- coding: utf-8 -*-
#
#  coder.py
#  
#  Copyright 2014 Gabriel Hondet <gabrielhondet@gmail.com>
#  
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
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
    '''
    Speed calculating :
    3.2 comes from 3.6 * 4 * 0.22222222222
    3.6 : m/s to km/h
    4 : one value each quarter of second
    0.222222222 : constant found by Adrien
    :returns: ewee's speed in km/h
    :rtype: float
    '''
    encoder_pin_1 = 23
    encoder_pin_2 = 24
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(encoder_pin_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(encoder_pin_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    temps = 0
    vitesse = 0
    last_encoded = 0
    MSB = 0
    LSB = 0
    circonference = 0.6283

    global encoder_value
    GPIO.add_event_detect(encoder_pin_1, GPIO.RISING, callback=update_encoder)
    GPIO.add_event_detect(encoder_pin_2, GPIO.RISING, callback=update_encoder)
    temps = time.time()



    while True:
        try:
            compteur = (time.time() - temps)

            if compteur >= 0.25:
                vitesse = 3.6*4*0.2222222*encoder_value*circonference/96
                encoder_value = 0
                temps = time.time()

                print(round(vitesse, 4))

        except KeyboardInterrupt:
            sys.exit()

def update_encoder(channel):
    global encoder_value
    global last_encoded
    MSB = GPIO.input(encoder_pin_1)
    LSB = GPIO.input(encoder_pin_2)

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
