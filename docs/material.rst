==========
 MATERIAL
==========

Hardware
--------

All relevant hardware has been provided to us by Flightradar24.

Skysense v2
~~~~~~~~~~~

The Skysense v2 is a custom receiver with an industrial grade
Raspberry Pi under the hood. It is the newest receiver used by
Flightradar24. It has 2 IO-connectors: Ethernet and USB. The Ethernet
port is used for communication between the Skysense v2 and
Flightradar24’s network. Therefore our solution has to be able to work
with a single USB port to be viable for usage with the Skysense v2.

Raspberry Pi
~~~~~~~~~~~~

The Skysense v2 has a Raspberry Pi on the inside. It is not a strict
requirement from Flightradar24 that our product should work with the
Skysense v2. Since Flightradar24 also has a lot of plain Raspberry
Pi-receivers in usage we could create a product that works with the
Raspberry Pi. The difference is that with a regular Raspberry Pi we
have more IO-connectors to our disposal instead of the single USB-port
on the Skysense v2. Our goal is to create a product that works with
the Skysense v2 but if we run into too much trouble, a plain Raspberry
Pi is our plan B.

Pololu Micro Maestro 6-Channel USB Servo Controller
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Maestro is used to control the servos in the pan/tilt-platform
over USB. We will be using an open source python-library to
communicate with the Maestro from the Raspberry Pi.

ELP 5-50mm Varifocal Lens 1080P
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is the webcam that we have decided to use. It has a manual zoom
capability.

Adafruit Mini Pan-Tilt Kit
~~~~~~~~~~~~~~~~~~~~~~~~~~

This is a pan-tilt platform that comes with two pre-assembled servos
of the model SG-90.

UGREEN USB Hub Super Speed 4
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is a USB Hub that we plan to use in order to communicate with the
camera and control the pan-tilt platform via the Skysense v2.

Software
--------

Python
~~~~~~

Flightradar24 requested that we should use Python for developing the
major part of this project.

Python module Maestro
~~~~~~~~~~~~~~~~~~~~~

This is a module to control the Maestro which we are planning to
use. The source code is under MIT-license which means we can use it
without many restrictions.

NodeJS Web server
~~~~~~~~~~~~~~~~~

To host the frontend live stream page we will use a NodeJS web server
with some common web technology (HTML/CSS/JavaScript).

Camera streaming software ffmpeg
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The camera streaming software will be ffmpeg and ffserver.

Python module Numpy
~~~~~~~~~~~~~~~~~~~

A module for computations and linear algebra providing vector types,
trigonometric functions, least squares solvers and many other useful
functions. The module is open source, under a license permitting
modification and commercial use.

Interface
---------

We will build an interface (probably web) to access the video stream
at a later stage in the project. We will probably use NodeJS for this
since it was proposed by Flightradar24.

Services
--------

We might need to use some cloud service at later stages in the
project. Flightradar24 would prefer if we used AWS since they already
use numerous services from Amazon.
