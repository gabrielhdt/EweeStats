#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#  pinselection.py
#  
#  Copyright 2014 Gabriel Hondet <gabrielhondet@gmail.com>
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#

from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
import os
import sys

def display_selection(analogSensors, lcd):
    """
    :param analogSensors: nombre de capteurs
    :type analogSensors: integer
    
    :param lcd: classe lcd
    :type lcd: Adafuit_CharLCDPlate()
    
    :returns: numéro de l'entrée analogique à afficher
    :rtype: integer
    """
    
    displayPin = 0
    
    if lcd.buttonPressed(lcd.UP) == 1:
        print('--UP PRESSED--')
        displayPin += 1
    elif lcd.buttonPressed(lcd.DOWN) == 1:
        print('--DOWN PRESSED--')
        displayPin -= 1
        
    if displayPin > analogSensors:
        displayPin = 0
        
    return displayPin
