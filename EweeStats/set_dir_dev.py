#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#  set_dir_dev.py
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
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from pyfirmata import Arduino, util
import time
import RPi.GPIO as GPIO
#import coder

def open_files(config):
    """
    :param config:  0 - number of sensors
                    1 - sensors id
                    2 - save_dir
                    3 - graph_name
                    4 - datas not graphed
                    5 - list of additionzl values id
                    6 - number of additional values
                    7 - pins to coder
    :type config: tuple
    
    :returns: tuple containing :
                0 - list of files for analogue datas
                1 - timestamp file
                2 - list of files for additional values
                3 - file for coder
    :rtype: tuple
    """
    
    file_list = []
    for i in range(config[0]):
        filename_tmp = "data_{i}".format(i = str(i))
        filepath_tmp = os.path.join(config[2], filename_tmp)
        data_file_tmp = open(filepath_tmp, 'w+')
        file_list.append(data_file_tmp)

    filepath_tmp = os.path.join(config[2], 'timestamp')
    time_file = open(filepath_tmp, 'w+')
    print(file_list)
    
    additional_files = []
    add_values_id = config[5] # Shortcut to avoid list in tuple
    for i in range(config[6]):
        filename_tmp = add_values_id[i]
        filepath_tmp = os.path.join(config[2], filename_tmp)
        add_file_tmp = open(filepath_tmp, 'w+')
        additional_files.append(add_file_tmp)

    # Coder file
    filepath_tmp = os.path.join(config[2], 'coder')
    coder_file = open(filepath_tmp, 'w+')
    
    file_config = (file_list, time_file, additional_files, coder_file)
    
    return file_config
    
def open_dev(encoder_pins):
    '''
    Opens communication with Arduino, GPIO and lcd
    :param encoder_pins: contains the GPIO pins to the encoder
    :type encoder_pins: list of integer
    
    :returns: lcd object, arduino object and iterator
    :rtype: tuple
    '''
    # LCD
    lcd = Adafruit_CharLCDPlate()
    lcd.clear()
    
    # GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(encoder_pins[0], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(encoder_pins[1], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    # Arduino
    # Init Arduino and iterator
    lcd.message("Connection de \nl'Arduino ...")
    board = Arduino('/dev/ttyACM0')
    lcd.clear()
    print('Arduino connected')
    lcd.message("Arduino connecte !")
    # Création itérateur
    iter8 = util.Iterator(board)
    iter8.start()
    
    dev = (lcd, board, iter8,)
    return dev

def set_arduino(number_sensors, board, iter8):
    """
    Set arduino to use
    :param number_sensors: number of analogue sensors wired
    :type number_sensors: integer
    
    :param board: object to control Arduino
    :type board: arduino class
    
    :param iter8: iterator to avoid buffer overflow of arduino
    :type iter8: I don't know
    
    :returns: 0
    """
    # Start listening ports
    for i in range(number_sensors):
        board.analog[i].enable_reporting()

    # Wait for a valid value to avoid None
    start = time.time()
    while board.analog[0].read() is None:
            print("nothing after {t}".format(t = time.time() - start))

    print("first val after {t}".format(t = time.time() - start))
    
    return 0



