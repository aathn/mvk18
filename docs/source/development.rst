==============
 DEVELOPMENT
==============

#############
CHANGELOG
#############

Sprint 1 (15/1 - 22/1)
--------
- Researched viable hardware to see what options we had
- Ordered hardware (two servos, a servo controller and a camera)
- Put up our trello board and Slack channel

Sprint 2 (22/1 - 4/2)
--------
- Decided on a git workflow
- Researched the preexisting skysense software
- Made a coordinate converter to convert the coordinates in the skysense to a usable format
	-  Satisfied FREQ_22, FREQ_8
- Received and tested the pan/tilt-platform

.. figure:: ../resources/camera2.jpg

   Our first setup using the pan/tilt-platform, the servo and the camera

Sprint 3 (4/2 - 15/2)
--------
- Worked on methods to handle multiple aircraft and calculate which aircraft was in view in an abstract manner
	- Partly satisfied QREQ_6
- Wrote code to extrapolate upcoming positions of an aircraft based on previous positions
	- Satisfied FREQ_13
- Wrote corde to convert from coordinates to a direction to point the camera
	- Satisfied FREQ10, FREQ11
- Learned how to control the pan/tilt-servos using an open source python library
	- Satisfied QREQ_8, FREQ_7
- Discussed software license with Flightradar24.

Sprint 4 (15/2 - 4/3)
--------
- Researched software that would be able to stream webcam footage to a web server
- Wrote code to parse the airplane data file to usable data within our program
- Made improvement to the code converting coordinates
- Managed to control the pan/tilt-servos directly from the skysense hardware

Sprint 5 (4/3 - 19/3)
--------
- Mounted the camera onto the platform
- Made a program to stream video from the camera
	- Satisfied FREQ_2
- Made a program to control the pan/tilt-servos
- Made a program to control the camera filming
	- FREQ_15, FREQ_16
- Made a simple interface to show the video that was being streamed
	- Satisfied FREQ_5
- Wrote tests for all of the finished code
- Split our program to work in multiple threads

.. figure:: ../resources/setup1.jpg

   Our first functional setup in action filming actual airplanes


Sprint 6 (19/3 - 4/4)
--------
- Created a basic configuration file which held the directional angle for the camera and the accepted view angles
	- Satisfied FREQ_18, FREQ_19
- Researched stream services.

Sprint 7 (4/4 - 5/9)
--------
- Tweaked plane selection to only select planes when they are within a certain distance
	- Satisfied QREQ_6, FREQ_12
- Ordered some new hardware (plattform and servos) in an attempt to get less shaky and more precise video output
- Installed this new hardware and calibrated the software to work with the new servos
- Made improvements to the configuration file to include stream settings
- Implemented a feature to display the aircraft id with the video stream on the web interface

#############
DEVELOPMENT DECISIONS
#############

Hardware
--------
During the first sprint the camera was decided based on price, size and ability to film in a quality that is good enough for our requirements.
The initial servos were chosen because we thought they would be strong enough and the price was low.
The first servos proved to be too weak to efficiently handle the weight of the camera, so new servos were ordered and mounted.
They were of a stronger model and solved the problems with previous servos.
The servo controller was chosen to make sure that it would be compatible with any servo hardware and work on the Skysense Linux system.

Software
--------
Python was chosen for writing the main program, since that was suggested by FR24 and since it was thought to cover the needs, which it did.

Initially there was a focus on streaming video to a local server instead of streaming to a cloud service provider (AWS).
That resulted in a lot of time spent on researching things that weren't really relevant to the final product.
It would have been wiser to study AWS services from the beginning, since time was very limited in the end of the project.

#############
REQUIREMENT VERIFICATION
#############

All requirements of the highest priority were satisfied, however, some of them were slightly modified over the development process.
Some of the lower priority requirements were not satisfied for various reasons.

The following requirements were partially changed during development:
- Airplane selection: FREQ_9
  Initially the plan was to not film airplanes that were going away from the camera, and instead focus on the ones approaching the camera. However, after discussing it with Flightradar24 we came to the conclusion that it would be effective enough to just film airplanes while they're within a certain radius.
- Keep selected airplane in view: FREQ_12
- Configurable view: FREQ_17
- Configuration process: FREQ_19
  Initially the plan was to have a way of configuring through some more sophisticated process, such as configuring the settings through a website. We later changed the requirement to accept that the process was simply to edit a config file.

The following lower priority requirements were not satisfied:
- Send data to cloud: FREQ_3
  Some effort was put in to reseraching the use of Amazon Kinesis (a video streaming service provided by AWS) to distribute the video stream. The process of streaming video footage to with Kinesis turned out to be quite complicated. It definitely appeared to be duable but due to time constraints we focused on other things.
- Store video in cloud: FREQ_4
  This requirement was dependent on the Send data to cloud-requirement.
- Avoid sun damage: FREQ_14
  We were unable to find a good way of doing this in the available time. We considered the option of reading the pixles on the screen to measure light level, but the streaming feature we used did not allow to do this easily.
- Display stored video on web page: FREQ_6
- Filter among previous recordings: FREQ_21
