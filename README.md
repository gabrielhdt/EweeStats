EweeStats - README
==================

Abstract
--------

EweeStats is a program designed to collect as much informations as possible from a vehicle on which sensors have been put.
It reads datas, processes it, diplays it and broadcasts it in a SVG [pygal](http://pygal.org) graph via http with [lighttpd](http://www.lighttpd.org).

This is a developpement version, it is not intended to be used out of the box !

pygal: http://pygal.org/

lighttpd: http://www.lighttpd.net/

Material required
-----------------

This program is designed to work with :

* a portable computer (Raspberry Pi ideally, has to be embedded in the vehicle)
* an Arduino (embedded too)
* (optionnally) an Adafruit CharLCDPlate (you might want to change the code if you consider not using it)
* a LAN to view the graph

Dependencies
------------

* pygal
* pyfirmata
* pyserial
* smbus-cffi

It will only work with Python 2.7.

Installation
------------

with pip :

`pip install EweeStats`

or from source :

`git clone https://github.com/gabrielhdt/EweeStats.git`

`python setup.py install`

Documentation
-------------

http://pythonhosted.org/EweeStats

History
-------

This program has been developped for the Baccalauréat exam.
