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

def create_files(save_dir, graph_path):
    """
    :returns: graphname
    :rtype: string
    """
    
    print(save_dir)
    print(graph_path)
    print(type(save_dir))
    print(type(graph_path))

    # Create directory to save datas
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
    
    # Create graph symlink
    web_root = '/var/www'
    #if os.path.isfile(os.path.join(web_root, graph_path)):
    #            os.remove(os.path.join(web_root, graph_path))
    #os.symlink(graph_path,
    #           os.path.join(web_root, graph_path))

def open_files(config):
    """
    :param config:  0 - number of sensors
                    1 - sensors id
                    2 - save_dir
                    3 - graph_name
    :type config: tuple
    
    :returns: list of opened files
    :rtype: list
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
    
    return file_list, time_file
    
def open_dev():
    """
    Opens communication with Arduino and lcd
    :returns: lcd object, arduino object and iterator
    :rtype: tuple
    """
    # LCD
    lcd = Adafruit_CharLCDPlate()
    lcd.clear()
    
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
    """Set arduino to use"""
    # Start listening ports
    for i in range(number_sensors):
        board.analog[i].enable_reporting()

    # Wait for a valid value to avoid None
    start = time.time()
    while board.analog[0].read() is None:
            print("nothing after {t}".format(t = time.time() - start))

    print("first val after {t}".format(t = time.time() - start))
    
    return 0



