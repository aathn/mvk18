==============
 TESTS
==============
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

.. needtable::
    :types: test
    :columns: title;status;incoming;tags;content
