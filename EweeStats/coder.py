#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#

import pyfirmata
import os
import sys
import shlex
import re
import time

def coder():
    board = pyfirmata.Arduino('/dev/ttyACM1')
    coder_pin_1 = 2
    coder_pin_2 = 3
    lastMSB = 0
    lastLSB = 0
    speed = 0.
    circonference = 0.62
    last_op = 0
    encoder_value = 0
    MSB = 0
    LSB = 0
    last_encoded = 0

    print(type(MSB))
    print(type(LSB))

    board.digital[coder_pin_1].write(1)
    board.digital[coder_pin_2].write(1)
    pin1 = board.get_pin('d:3:i')
    pin2 = board.get_pin('d:2:i')

    while True:
        try:
            compteur = time.time() - last_op
            if compteur >= 1:
                speed = encoder_value*circonference/96
                encoder_value = 0
                last_op = time.time()
                print('Speed : {s}'.format(s = speed))

#            MSB = board.digital[2].read()
#            LSB = board.digital[3].read()
            MSB = pin1.read()
            LSB = pin2.read()
            print('MSB : {m} et LSB : {l}'.format(m = MSB, l = LSB))

            if  (MSB != lastMSB) or (LSB != lastLSB):
                encoded = (MSB << 1) |LSB
                sum_coded = (last_encoded << 2) | encoded
                if (sum == 0b1101 or sum == 0b0100 or sum == 0b0010 or sum == 0b1011):
                    encoder_value += 1

                if (sum == 0b1110 or sum == 0b0111 or sum == 0b0001 or sum == 0b1000):
                    encoder_value -=1

                last_encoded = encoded
                lastMSB = MSB
                lastLSB = LSB

        except KeyboardInterrupt:
            board.exit()
            sys.exit()


if __name__ == '__main__':
    coder()
