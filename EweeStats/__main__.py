#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#  __main__.py
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
import set_dir_dev
import AnalogGraphThreads
import readconfig


def main():
    
    config = readconfig.read_config()
    # config contains : number_sensors, sen_id, save_dir, graph_name
    
    # Create files
    set_dir_dev.create_files(config[2], config[3])
    # Opens them
    file_list, time_file = set_dir_dev.open_files(config)
    # Opens devices
    dev = set_dir_dev.open_dev()
    # dev contains : lcd, board, iter8
    set_dir_dev.set_arduino(config[0], dev[1], dev[2])

    # Create threads
    data2Graph = AnalogGraphThreads.AnalogGraphThreads(config[0])
    data2Graph.startThreads(config, dev, file_list, time_file)
    
    
    return 0

if __name__ == '__main__':
    main()

