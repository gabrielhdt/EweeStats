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
import create_files
import AnalogGraphThreads


def main():
    
    datapath = os.path.join('/home/pi', 'ewee_data')
    
    # Create files and open
    analogSensors = 2
    graph_name = create_files.create_files(datapath)
    file_list, time_file = create_files.open_files(
        analogSensors, datapath)

    # Create threads
    data2Graph = EweeStats.AnalogGraphThreads.AnalogGraphThreads(
        analogSensors, file_list, time_file, graph_name, datapath)
    data2Graph.startThreads()
    
    
    return 0

if __name__ == '__main__':
    main()
