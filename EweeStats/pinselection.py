# -*- coding: utf-8 -*-
#
#  pinselection.py
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


from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
import os
import sys
import time

def display_selection(number_analog_sensors, number_add_values, lcd, selected_pin):
    """
    :param number_analog_sensors: nombre de capteurs
    :type number_analog_sensors: integer
    
    :param lcd: classe lcd
    :type lcd: Adafuit_CharLCDPlate()
    
    :param selected_pin: sélection à la boucle d'avant
    :type selected_pin: integer
    
    :returns: what to display
    :rtype: list of 2 integers
    """
    
    
    # Read buttons activity
    if lcd.buttonPressed(lcd.UP):
        print('--UP PRESSED--')
        selected_pin += 1
    elif lcd.buttonPressed(lcd.DOWN):
        print('--DOWN PRESSED--')
        selected_pin -= 1
    elif lcd.buttonPressed(lcd.LEFT):
        selected_array += 1
    elif lcd.buttonPressed(lcd.LEFT):
        selected_array -= 1
    
    # If we go inferior than 0, go back to max, and the opposite
    if selected_pin >= number_analog_sensors and selected_array == 0:
        selected_pin = 0
    elif selected_pin < 0 and selected_array == 0:
        selected_pin = number_analog_sensors - 1  # -1 because pins start to 0
    elif selected_array == 1 and selected_pin >= number_add_values:
        selected_pin = 0
    elif selected_array == 1 and selected_pin <:
        selected_pin = number_add_values - 1
        
    return [selected_pin, selected_array]
