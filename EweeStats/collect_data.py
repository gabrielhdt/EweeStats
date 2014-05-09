# -*- coding: utf-8 -*-
#
#  collect_data.py
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

def collecting(
    board, sensor_id_list, analogSensors):
    """
    :param board: object Arduino
    :type board: Arduino class
    
    :param sensor_dict: dictionnary containing sensors type
    :type sensor_dict: dict
    """
    value_list_instant = [0.0 for i in range(analogSensors)]
    values_converted_instant = value_list_instant
    
    for i in range(analogSensors):
        value_list_instant[i] = board.analog[i].read()
    
    for i, elt in enumerate(sensor_id_list):
        if elt == 'pot':
            values_converted_instant[i] = pot(value_list_instant, i)
        elif elt == 'coder':
            pass
        elif elt == 'accelerometer':
            pass
        elif elt == 'gyr':
            pass
        else:
            values_converted_instant[i] = value_list_instant[i]
    
    return values_converted_instant


def pot(value_list_instant, pin_pot):
    """
    :param pinToPot: numéro du pin relié au potentiomètre
    :type pinToPot: integer

    :param valueList: valeurs non transformées
    :type valueList: list

    :param valueReal: liste devant acceuillir les valeurs transformées
    :type valueReal: list

    :returns: nombre converti à la case du numéro du pin
    :rtype: integer
    """
    value_converted = value_list_instant[pin_pot] * 5

    return value_converted

def coder(value_list_instant, pin_coder):
    """
    :returns: translational speed
    :rtype: float
    """
    pass
    
def digital_through_analog(pin):
    """
    As digital read doesn't work, we need to use analogue pins
    
    :param pin: number of the pin reading
    :type pin: integer
    
    :returns: bit
    :rtype: boolean
    """
    if board.analog[pin].read() < 0.5:
        return 0
    elif board.analog[pin].read() >= 0.5:
        return 1
    else:
        return 0


