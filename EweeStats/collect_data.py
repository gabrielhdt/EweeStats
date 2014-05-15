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
    
    :param sensor_id_list: names of sensors
    :type sensor_id_list: list
    
    :param number_sensors: number of analog sensors
    :type number_sensors: int
    
    :param sensor_id_list: list containing sensors type
    :type sensor_id_list: list
    """
    value_list_instant = [0.0 for i in range(analogSensors)]
    values_converted_instant = value_list_instant
    additional_values = []
    
    for i in range(analogSensors):
        value_list_instant[i] = board.analog[i].read()
    
    # Loop to launch the right program to convert data
    for i, elt in enumerate(sensor_id_list):
        if elt == 'pot':
            values_converted_instant[i] = pot(value_list_instant[i])
        elif elt == 'coder':
            pass
        elif elt == 'accelerometer_x':
            accelerometer = True
            values_converted_instant[i] = accelerometer_x(value_list_instant[i])
        elif elt == 'accelerometer_y':
            accelerometer = True
            values_converted_instant[i] = accelerometer_y(value_list_instant[i])
        elif elt == 'accelerometer_z':
            accelerometer = True
            values_converted_instant[i] = accelerometer_z(value_list_instant[i])
        elif elt == 'gyr':
            pass
        elif elt == 'voltage':
            values_converted_instant[i] = voltage(value_list_instant[i])
        elif elt == 'compass':
            values_converted_instant[i] = compass(value_list_instant[i])
        elif elt == 'tilt':
            pass
        else:
            values_converted_instant[i] = value_list_instant[i]
    
    if accelerometer:
        additional_values.append(accel_norme)
    
    return values_converted_instant


def pot(value_instant):
    """
    :param pin_pot: numéro du pin relié au potentiomètre
    :type pin_pot: integer

    :param value_list_instant: valeurs non transformées
    :type value_list_instant: list

    :returns: converted value of voltage
    :rtype: integer
    """
    value_converted = value_instant*5

    return value_converted, additional_values

def coder(value_instant):
    """
    :returns: translational speed
    :rtype: float
    """
    pass
    
def voltage(value_instant):
    """
    :param value_instant: value measured
    :type value_instant: list

    :param pin_voltage: pin on which is wired the sensor
    :type pin_voltage: integer

    :returns: voltage
    :rtype: float
    """
    voltage = 0.0933*pow(value_instant, 0.961)
    return voltage

def tilt(s1, s2):
    """
    :param s1: value of first pin
    :type s1: boolean

    :param s2: value of second
    :type s2: boolean

    :returns: position 0, 1, 2 or 3
    :rtype: int
    """
    pos = (s1 << 1) | s2
    return pos
    
def accelerometer_x(x_raw):
    """
    :param x_raw: value from arduino
    :type x_raw: float
    
    :returns: acceleration on x axis
    :rtype: float
    """
    x_accel = (x_raw - 0.3646)*130.106
    return x_accel

def accelerometer_y(y_raw):
    y_accel = (y_raw - 0.3646)*130.106
    return y_accel
    
def accelerometer_z(z_raw):
    z_accel = (z_raw - 0.3646)*130.106
    return z_accel

def accel_norme(x_accel, y_accel, z_accel):
    norme = math.sqrt(
        pow(x_accel, 2) + pow(y_accel, 2) + pow(z_accel, 2)
        )
    return norme
