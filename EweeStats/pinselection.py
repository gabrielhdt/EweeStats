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

def display_selection(number_analog_sensors, number_add_values, lcd, selected_value):
    """
    :param number_analog_sensors: nombre de capteurs
    :type number_analog_sensors: integer

    :param number_add_values: number of additional values
    :type number_add_values: integer
    
    :param lcd: classe lcd
    :type lcd: Adafuit_CharLCDPlate()
    
    :param selected_pin: sélection à la boucle d'avant
    :type selected_pin: integer

    :param selected_value:  0 - selected_array (calculated values or analogue)
                            1 - selected value in the array
    :type selected_values: list of 2 integers
    
    :returns: what to display : selected_values
    :rtype: list of 2 integers

    Currently 3 arrays : 0 for analogue values, 1 for calculated ones
    and 2 for encoder
    """
    
    # Number of arrays, to be sure not to display an inexistant one
    number_arrays = 3 
    # Read buttons activity
    if lcd.buttonPressed(lcd.UP):
        print('--UP PRESSED--')
        selected_value[1] += 1
    elif lcd.buttonPressed(lcd.DOWN):
        print('--DOWN PRESSED--')
        selected_value[1] -= 1
    elif lcd.buttonPressed(lcd.RIGHT):
        selected_value[0] += 1
    elif lcd.buttonPressed(lcd.LEFT):
        selected_value[0] -= 1
    
    # Managing if array displayed array exists
    if selected_value[0] >= number_arrays:
        selected_value[0] = 0
    elif selected_value[0] < 0:
        selected_value[0] = number_arrays - 1 # because arrays begin to 0

    # If we go inferior than 0, go back to max, and the opposite
    if selected_value[0] == 0 and selected_value[1] >= number_analog_sensors:
        selected_value[1] = 0
    elif selected_value[0] == 0 and selected_value[1] < 0:
        selected_value[1] = number_analog_sensors - 1  # -1 because pins start to 0
    elif selected_value[0] == 1 and selected_value[1] >= number_add_values:
        selected_value[1] = 0
    elif selected_value[0] == 1 and selected_value[1] < 0:
        selected_value[1] = number_add_values - 1
    elif selected_value[0] == 2 and selected_value[1] >= 1:
        selected_value[1] = 0 # If someone wants to add data with encoder
    elif selected_value[0] == 2 and selected_value[1] < 0:
        selected_value[1] = 0
        
    return selected_value
