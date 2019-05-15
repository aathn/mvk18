.. _appendix-a:

============
 APPENDICES
============

A: Requirements and Tests
=========================

This section provides detailed descriptions of all tests and
requirements, functional and nonfunctional.

Requirements
------------

.. req:: Capture video
   :id: FREQ_1
   :tags: functional
   :status: done 2019-04-03
   :links: QREQ_1; TEST_3; TEST_7
   :priority: 1

   The software shall be capable of receiving continuous video output from a camera.

.. req:: Captured video quality
   :id: QREQ_1
   :tags: quality

   The software should be able to handle a video stream of 1280x720
   mpeg video with at least 15 fps for at least 10 minutes
   continuously.

.. req:: Stream video
   :id: FREQ_2
   :tags: functional
   :status: done 2019-04-03
   :links: QREQ_2; TEST_3; TEST_7
   :priority: 1

   Our software shall send the captured video to an output URL / file.

.. req:: Streamed video quality
   :id: QREQ_2
   :tags: quality

   The software should be able to output the video
   stream received from the camera continuously at a bit rate of
   1000kb/s

.. req:: Send data to cloud
   :id: FREQ_3
   :tags: functional
   :status: incomplete
   :priority: 2

   The video data of streamed flights shall be sent to a cloud service provider

.. req:: Store video in cloud
   :id: FREQ_4
   :tags: functional
   :status: incomplete
   :priority: 3

   The video sent shall be stored in the cloud and organised in a
   database.

.. req:: Display streams on web page
   :id: FREQ_5
   :tags: functional
   :status: done 2019-04-03
   :links: TEST_3; TEST_7
   :priority: 2

   The web user shall be able to see all current streams on a web page
   along with relevant information.

.. req:: Display stored video on web page
   :id: FREQ_6
   :tags: functional
   :status: incomplete
   :priority: 3

   The web user shall be able to see a list of previously recorded
   flights on a web page.

.. req:: Filter among previous recordings
   :id: FREQ_21
   :tags: functional
   :status: incomplete
   :priority: 4

   The web user shall be able to filter previous recordings after
   flight number and other information.

.. req:: Control the servo
   :id: FREQ_7
   :tags: functional
   :status: done 2019-02-13
   :links: QREQ_3; TEST_2; TEST_7
   :priority: 1

   The pan/tilt servo shall take two input angles and move the camera
   to pan and tilt in those angles.

.. req:: Pan/tilt servo accuracy
   :id: QREQ_3
   :tags: quality

   The pan/tilt servo should be calibrated in such a way that the
   difference between input angles and output angles is not greater
   than 0.05 radians

.. req:: Data parsing
   :id: FREQ_8
   :tags: functional
   :status: done 2019-02-28
   :links: TEST_4
   :priority: 1

   The Skysense shall parse (JSON) data from all flights into a format
   directly supported by the software

.. req:: Airplane selection
   :id: FREQ_9
   :tags: functional
   :status: done 2019-03-26
   :links: QREQ_4; TEST_7
   :priority: 1

   The skysense shall automatically pick one airplane from the parsed
   data

.. req:: Airplane selection criteria
   :id: QREQ_4
   :tags: quality

   The software shall prioritize airplanes that are within 40,000 feet
   (~12 km)

.. req:: Convert GPS coordinates to relative positions
   :id: FREQ_10
   :tags: functional
   :status: done 2019-03-26
   :links: TEST_6; TEST_10
   :priority: 1

   Our software shall be able to translate the GPS-position of
   airplanes to a position relative to the camera using a horizontal coordinate
   system

.. req:: Convert relative positions to angles
   :id: FREQ_11
   :tags: functional
   :status: done 2019-03-13
   :links: QREQ_5; TEST_1; TEST_12
   :priority: 1

   The relative position shall be translated to camera pan/tilt angles
   instructing the camera where to point.

.. req:: Conversion accuracy
   :id: QREQ_5
   :tags: quality

   The conversion of relative position to pan/tilt angle shall be
   achieved with a precision within 0.05 radians.

.. req:: Keep selected airplane in view
   :id: FREQ_12
   :tags: functional
   :status: done 2019-03-26
   :links: QREQ_6; TEST_9
   :priority: 1

   Our software should control the servo to keep the selected airplane
   in the frame of view when possible

.. req:: Airplane tracking quality
   :id: QREQ_6
   :tags: quality

   The servo position should be updated frequently enough to avoid
   jagged movement. It should also keep the airplane centered in the
   field of view.

.. req:: Predict flight path by extrapolating
   :id: FREQ_13
   :tags: functional
   :status: done 2019-03-13
   :links: QREQ_7; TEST_5; TEST_12
   :priority: 1

   The software shall to be able to predict flight paths to make up
   for any lack of continuity in the received data.

.. req:: Extrapolation accuracy
   :id: QREQ_7
   :tags: quality

   The extrapolation should be accurate for airplanes following a
   linear trajectory. That is, requirement :need:`QREQ_6` should be
   fulfilled for an airplane following such a trajectory even when new
   data is not being received continuously.

.. req:: Avoid sun damage
   :id: FREQ_14
   :tags: functional
   :status: incomplete
   :priority: 2

   The camera shall never point directly towards the sun to avoid
   being damaged.

.. req:: Automatically start streaming
   :id: FREQ_15
   :tags: functional
   :status: done 2019-04-03
   :links: TEST_3; TEST_7
   :priority: 1

   The software should automatically start a video stream when there
   is a visible airplane in view.

.. req:: Automatically stop streaming
   :id: FREQ_16
   :tags: functional
   :status: done 2019-04-03
   :links: TEST_3; TEST_7
   :priority: 1

   The software should automatically stop streaming when there no
   longer are any visible airplanes in view.

.. req:: Configurable view
   :id: FREQ_17
   :tags: functional
   :status: done 2019-04-02
   :links: TEST_11; TEST_12
   :priority: 1

   The host shall be able to define the camera's view angle, to enable
   the camera to only track visible airplanes.

.. req:: Abide view boundaries
   :id: FREQ_18
   :tags: functional
   :status: done 2019-04-02
   :links: TEST_11; TEST_12
   :priority: 1

   The camera shall not move outside of the host's defined view angle.

.. req:: Configuration process
   :id: FREQ_19
   :tags: functional
   :status: done 2019-04-02
   :priority: 2

   The host shall be able to set the direction and view angle of the
   camera using a configuration file.

.. req:: Non-dependability on hardware
   :id: QREQ_8
   :tags: quality

   To make it easier for Flightradar24 to keep developing after the
   course is finished, the software should be as indepedent on the
   specific hardware components as possible.

.. req:: Ensure that streaming is scalable
   :id: QREQ_9
   :tags: quality

   The streaming setup should be scalable in order to able to keep up
   with a growing number of viewers.

.. req:: Get own GPS position
   :id: FREQ_22
   :tags: functional
   :status: done 2019-04-02
   :links: TEST_8
   :priority: 1

   The software shall be able to get its own GPS position from a file
   on the skysense system.

Tests
-----

.. test:: Radians to servo values
    :id: TEST_1
    :tags: unittest
    :status: passing

    A python class consisting of methods that convert radian angles to
    values that can be understood by the servo. Deemed to pass when
    angles are converted to the expected values.

.. test:: Servo movement test
    :id: TEST_2
    :tags: manual
    :status: passing

    A python program that moves the servo to its extreme angles. The
    pan/tilt servo is observed and the test is passed if the servo
    moves as expected. For accuracy measurements a protractor should
    be used.

.. test:: Video stream test
    :id: TEST_3
    :tags: manual
    :status: passing

    Test is passed when we can observe the camera software (FFmpeg)
    processes the camera input and outputs a visible stream to our web server.

.. test:: Basic airplane parsing
    :id: TEST_4
    :tags: unittest
    :status: passing

    A set of unit tests testing the basic parsing functionality from
    JSON to Python dicts: Parsing of empty files, files with a single
    airplane, and files with several airplanes.

.. test:: Own position parsing
    :id: TEST_8
    :tags: unittest
    :status: passing

    A unit test ensuring that the software is able to parse its own
    position correctly from a file.

.. test:: Continuous updating of camera airplanes
    :id: TEST_9
    :tags: unittest
    :status: passing

    A unit test ensuring that the parsing functionality can be
    continuously executed in a separate thread, keeping the camera's
    airplane positions updated.

.. test:: Extrapolation of airplane coordinates
    :id: TEST_5
    :tags: unittest
    :status: passing

    A unit test testing that the extrapolation of airplane coordinates
    is exact for an airplane following a linear trajectory. Passed
    when extrapolated function values are same as original function
    values.

.. test:: Conversion from GPS-coordinates to ECEF
    :id: TEST_6
    :tags: unittest
    :status: passing

    A set of unit tests ensuring that the first step of conversion
    from GPS coordinates to relative coordinate works correctly. In
    this first step, GPS coordinates are converted to earth-centerd,
    earth-fixed (ECEF) cartesian coordinates. Tests that values are
    converted correctly for a wide range of inputs.

.. test:: Conversion from GPS-coordinates to relative positions
    :id: TEST_10
    :tags: unittest
    :status: passing

    A set of unit tests testing the entire process of converting GPS
    coordinates to relative positions. Tests that values are converted
    to their corresponding relative camera positions (azimuth,
    vertical angle, distance) for a wide range of values.

.. test:: Main functionality
    :id: TEST_7
    :tags: manual
    :status: passing

    A program simulating an airplane passing overhead, testing that the
    camera follows and streams it, verifying that all main pieces of
    functionality work and communicate correctly.

.. test:: Configurable view tests
    :id: TEST_11
    :tags: unittest
    :status: passing

    A suite of unit tests testing that planes inside or outside the
    specified view range are identified as such.

.. test:: Camera class tests
    :id: TEST_12
    :tags: unittest
    :status: passing

    A suite of unit tests making sure that coordinate conversion
    functions and camera view configuration are correctly incorporated
    into the object oriented Camera class.
