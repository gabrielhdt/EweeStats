# -*- coding: utf-8 -*-
#
#  readconfig.py
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
import re
import shlex

def read_config():
    """
    Reads configuration file to set up sensors
    
    :returns: tuple containing :
                0 - number of sensors
                1 - list id of sensors (indice is pin and name is type)
                2 - save directory
                3 - name of the graph
                4 - pins to be graphed
                5 - list of additional values id
                6 - number of additional_values
                7 - list of two pins for encoder
    :rtype: tuple
    """
    conf_file = os.path.join(
        '/etc/eweestats', 'eweestats.conf')
    
    if not os.path.isfile(conf_file):
        raise NameError('no configuration file')
        sys.exit()
    
    pin_to_graph = [] # List to indicate if values shouldn't be graphed
    add_values_id = [] # List for id of additional values
    number_add_values = 0 # Number of additional values
    encoder_pins = [0, 0] # List for two pins of encoder
    
    # Reads the file
    with open(conf_file, 'r') as c:
        for line in c:
            part = shlex.split(line, True)
            if part == []:
                continue
            print(part)
            # Number of sensors
            if re.search(r'sensors', part[0]) is not None:
                number_sensors = int(part[2])
                sensors_id = [0 for i in range(number_sensors)]
            # Type of sensors
            elif re.match(r'^A[0-9]{1,2}$', part[0]) is not None:
                # Searche for A and one or two numbers
                pin_number = int(part[0].replace('A', ''))
                sensors_id[pin_number] = part[2]
            # Save directory
            elif re.match(r'^savedir', part[0]) is not None:
                save_dir = part[2]
            # Name of graph
            elif re.match(r'^graphname', part[0]) is not None:
                graph_name = part[2]
            # Datas to graph
            elif re.search(r'pin_to_graph', part[0]) is not None:
                pin_to_graph.append(int(part[2]))
            # Digital sensors
            elif re.search(r'e1', part[0]) is not None:
                encoder_pins[0] = int(part[2])
            elif re.search(r'e2', part[0]) is not None:
                encoder_pins[1] = int(part[2])
    
    # Check sensors for additional datas
    for elt in sensors_id:
        if re.search(r'accel', elt) is not None:
            is_accel = [False, False, False] # Booleans to check axis
    # When axis is found, it is marked as existant
    for elt in sensors_id:
        if elt == 'accelerometer_x':
            is_accel[0] = True
        elif elt == 'accelerometer_y':
            is_accel[1] = True
        elif elt == 'accelerometer_z':
            is_accel[2] = True
    # If there are 3 axis, we can calculate norm
    if is_accel == [True, True, True]:
        add_values_id.append('accel_norm')
        number_add_values += 1
    
    graph_name = os.path.join(save_dir, graph_name)
    #print(number_sensors)
    print('Sensors id :')
    print(sensors_id)
    print('Save directory :')
    print(save_dir)
    print(graph_name)
    #print(pin_to_graph)
    #print(add_values_id)
    #print(is_accel)
    #print(number_add_values)
    print('Encoder pins :')
    print(encoder_pins)
    
    config = (
        number_sensors, sensors_id, save_dir, graph_name,pin_to_graph,
        add_values_id, number_add_values, encoder_pins)
    return config
    
if __name__ == '__main__':
    read_config()
