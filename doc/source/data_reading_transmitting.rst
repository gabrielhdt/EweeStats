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

.. py:function:: board = Arduino(id)

    :param id: chaîne de caractère de l'identifiant de l'arduino dans le répertoire /dev
    :type  id: string

    Crée la variable board de classe Arduino permettant d'opérer sur l'Arduino.

.. py:function:: board.analog[i].enable_reporting()

    :param i: numéro de l'entrée analogique
    :type i: integer

    Commence l'écoute d'une entrée analogique sur l'Arduino.

.. py:function:: board.analog[i].read()

    :param i: numéro de l'entrée analogique de l'Arduino
    :type i: integer

    Renvoit une valeur entre 0 et 1 correspondant à la tension aux bornes d'une entrée analogique.

