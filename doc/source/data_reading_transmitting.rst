Lecture et transmission des mesures
===================================
Pour lire les capteurs, ils ont été branchés à l'Arduino.
La transmission se fait par port USB, ce qui permet d'alimenter l'Arduino et de transférer les données rapidement, et assez facilement.

Transmission côté Arduino
-------------------------
Le programme Firmata a été utilisé. Une fois envoyé sur l'Arduino, celui-ci envoit tout ce qu'ils reçoit par le port USB.
Le programme est disponible en tant qu'exemple dans l'IDE Arduino, nommé StandardFirmata. Sinon, il est téléchargeable sur le site Firmata_.

.. _Firmata: http://firmata.org/wiki/Main_Page

Transmission côté Raspberry Pi
------------------------------
pyFirmata a ensuite été utilisé pour utiliser les données transmises par USB.

.. py:function:: Arduino(string)

    Ouvre la connection avec l'Arduino
