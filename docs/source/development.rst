==============
 DEVELOPMENT
==============

#############
CHANGELOG
#############

Sprint 1 (15/1 - 22/1)
--------
- We researched viable hardware to see what options we had
- We ordered hardware (two servos, a servo controller and a camera)
- We put up our trello board and Slack channel

Sprint 2 (22/1 - 4/2)
--------
- We decided on a git workflow
- We researched the preexisting skysense software
- We made a coordinate converter to convert the coordinates in the skysense to a usable format
- We received and tested the pan/tilt-platform

.. figure:: ../resources/camera2.jpg

   Our first setup using the pan/tilt-platform, the servo and the camera

Sprint 3 (4/2 - 15/2)
--------
- We worked on methods to handle multiple aircraft and calculate which aircraft was in view in an abstract manner
- We wrote code to extrapolate upcoming positions of an aircraft based on previous positions
- We wrote corde to convert from coordinates to a direction to point the camera
- We learned how to control the pan/tilt-servos using an open source python library
- We discussed software license with Flightradar24.

Sprint 4 (15/2 - 4/3)
--------
- We researched software that would be able to stream webcam footage to a web server
- We wrote code to parse the airplane data file to usable data within our program
- We made improvement to the code converting coordinates
- We managed to control the pan/tilt-servos directly from the skysense hardware

Sprint 5 (4/3 - 19/3)
--------
- We mounted the camera onto the platform
- We made a program to stream vido from the camera
- We made a program to control the pan/tilt-servos
- We made a program to control the camera filming
- We made a simple interface to show the video that was being streamed
- We wrote tests for all of the finished code
- We split our program to work in multiple threads

.. figure:: ../resources/setup1.jpg

   Our first functional setup in action filming actual airplanes


Sprint 6 (19/3 - 4/4)
--------
- We created a basic configuration file which held the directional angle for the camera and the accepted view angles
- We researched stream services.

Sprint 7 (4/4 - 5/9)
--------
- We ordered some new hardware (plattform and servos) in an attempt to get less shaky and more precise video output
- We installed this new hardware and calibrated the software to work with the new servos
- We made improvements to the configuration file to include stream settings
- We implemented a feature to display the aircraft id with the video stream on the web interface
