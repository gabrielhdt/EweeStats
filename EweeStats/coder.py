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
import time
import RPi.GPIO as GPIO
import globvar

def coder(circonference):
    '''
    Calculates speed
    3.2 comes from 3.6 * 4 * 0.22222222222
    3.6 : m/s to km/h
    10 : ten values per second
    0.222222222 : constant found by Adrien
    :returns: ewee's speed in km/h
    :rtype: float
    '''
    speed = 3.6*10*0.22222222*globvar.encoder_value*circonference/96
    globvar.encoder_value = 0
    return round(speed, 4)

def update_encoder(channel):
    '''
    Executed each change of value on coder pins
    '''
    MSB = GPIO.input(globvar.encoder_pins[0])
    LSB = GPIO.input(globvar.encoder_pins[1])

    encoded = (MSB << 1) |LSB
    sum = (globvar.last_encoded << 2) | encoded

    if (sum == 0b1101 or sum == 0b0100 or sum == 0b0010 or sum == 0b1011):
        globvar.encoder_value +=1
    if (sum == 0b1110 or sum == 0b0111 or sum == 0b0001 or sum == 0b1000):
        globvar.encoder_value -= 1

    globvar.last_encoded = encoded
    return 0


if __name__ == '__main__':
    coder()
