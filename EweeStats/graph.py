# -*- coding: utf-8 -*-
#
#  graph.py
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


import pygal
import os
import sys

def create_graph(config, all_values, all_add_values, timelist):
    """
    Creates graph thanks to pygal
    :param config: tuple containing :
                        0 : number of analogue sensors (integer)
                        1 : sensors id (list)
                        2 : save_dir (string)
                        3 : graph_name (string)
                        4 : sensors to graph (list)
                        5 : additional values id
                        6 : number of additional_values
                        7 : list of pins to coder
    :type config: tuple
    
    :param all_add_values: all calculated values
    :type all_add_values: list of floats
    
    :param all_values: all values
    :type all_values: list of lists of floats
    
    :param timelist: timestamp
    :type timelist: list of strings

    :returns: 0
    """
    # Shortcuts
    analogue_id = config[1]
    add_values_id = config[5]
    # Graph file name
    graphTempName = config[3].replace('.svg', '.svg.tmp')

    linechart                   = pygal.Line()
    linechart.x_label_rotation  = 20
    linechart.show_dots         = False
    linechart.human_readable    = True
    linechart.title             = 'Tension en fonction du temps'
    linechart.x_title           = 'Temps (s)'
    linechart.x_labels          = timelist
    linechart.x_labels_major_count = 20
    linechart.show_minor_x_labels = False
    # Add values from analogue pins
    for i in config[4]:
        linechart.add(
            '{ids} {p}'.format(ids = analogue_id[4],
            p = i), all_values[i]
            )
    # Add calculated values
    for i in range(config[6]):
        linechart.add(
            '{ids} {p}'.format(ids = add_values_id[i],
            p = i), all_add_values[i]
            )
    
    # We're creating a temp graph because pygal removes it when graph
    #   creation begins
    linechart.render_to_file(os.path.join(config[2], graphTempName))
    # Graph to be linked
    os.rename(os.path.join(config[2], graphTempName),
              os.path.join(config[2], config[3]))
    
    return 0

def coder(config, coder_values, interval):
    '''
    Graph coder datas
    :param config: tuple containing :
                        0 : number of analogue sensors (integer)
                        1 : sensors id (list)
                        2 : save_dir (string)
                        3 : graph_name (string)
                        4 : sensors to graph (list)
                        5 : additional values id
                        6 : number of additional_values
                        7 : list of pins to coder
    :type config: tuple
    
    :param coder_values: values to graph, speed in km/h
    :type coder_values: float
    
    :param interval: time between two measures in seconds
    :type interval: float
    '''
    # Create time axis
    timelist = [interval*i for i in range(len(coder_values))]
    
    # Create graph
    linechart = pygal.Line()
    linechart.x_label_rotation = 20
    linechart.show_dots = False
    linechart.human_readable = True
    linechart.title = 'Vitesse en fonction du temps'
    linechart.x_title = 'Temps (s)'
    linechart.y_title = 'Vitesse (km/h)'
    linechart.x_labels_major_count = 20
    linechart.show_minor_x_labels = False
    # Add datas to graph
    linechart.add('Vitesse', coder_values)
    
    linechart.render_to_file(os.path.join(config[2], 'EweeCoder.svg.tmp'))
    os.rename(os.path.join(config[2], 'EweeCoder.svg.tmp'),
              os.path.join(config[2], 'EweeCoder.svg'))
    
