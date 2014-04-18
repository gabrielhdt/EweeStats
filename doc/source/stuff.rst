Matériel utilisé
================

Le matériel devait être :
    * pas trop cher
    * léger et peu énergivore pour pouvoir être embarqué dans l'Ewee
    * interfaçable pour connecter un assez grand nombre de capteurs facilement
    * assez puissant pour traiter, présenter un grand nombre de données et les diffuser
C'est pourquoi nous avons utilisé :
    * Raspberry Pi
    * Arduino
    * Affichage LCD

Arduino
-------
L'Arduino est sûrement la carte la plus interfaçable qui existe, et à un prix largement abordable. Néanmoins, étant limitée au niveau puissance, on a préféré l'utiliser uniquement pour prendre les mesures
L'Arduino utilisée lors du développement est une Uno rev3.


Raspberry Pi
------------
Nous avons pris une Raspberry Pi car elle est bien plus puissante qu'une Arduino, et étant un mini ordinateur, elle est capable d'interpréter divers langages de programmation. Utilisant GNU/Linux Debian, ou plus précisément Raspbian, elle se connecte facilement à internet et bénéficie de la diversité des logiciels proposés en open-source pré-compilés pour la distribution.
Est utilisé un modèle B avec raspbian sur une carte SD classe 10_.

.. _10: http://http://fr.wikipedia.org/wiki/Carte_SD#D.C3.A9bit/

Affichage LCD
-------------
Pour communiquer rapidement les données, nous avons choisi d'utiliser un écran LCD adapté à la Raspberry Pi.
L'écran proposé par Adafruit_ permet d'afficher 32 caractères (16 sur 2 lignes) ce qui paraît insuffisant pour toutes les mesures, mais il dispose également de boutons, permettant de faire défiler les mesures, rendant les 32 caractères parfaitement adéquats

.. _Adafruit: https://learn.adafruit.com/adafruit-16x2-character-lcd-plus-keypad-for-raspberry-pi/overview/
