==============
 TESTS
==============
.. test:: Radians to servo-angles test
   :id: TEST_1
   :tags: unittest
   :status: passing

   A python class consisting of methods that convert radian angles to angles that can be understood by the servo.
   Passed when values are converted to expected values.

.. test:: Servo movement test
    :id: TEST_2
    :tags: manual
    :status: passing

    A python program that moves the servo to its extreme angles.
    The pan/tilt servo is observed and the test is passed if the servo moves as expected.
    For accuracy a goniometer should be used.

.. test:: Video stream test
   :id: TEST_3
   :tags: manual
   :status: passing

   Test is passed when we can observe the camera software (FFmpeg)
   processes the camera input and outputs a visible stream to our web server.

.. test:: Parsing test
  :id: TEST_4
  :tags: unittest
  :status: passing

  A python class (ParserTests) testing all sorts of parsing from JSON to Python dicts:
  Parsing of single airplanes data, several airplanes data and of skysense position data.

.. test:: Extrapolation of airplane coords test
  :id: TEST_5
  :tags: unittest
  :status: passing

  A python class (AirplaneTests) testing if the extrapolation of airplane coords returns expected coords when time changes.
  Passed when asserted values are same as actual values.

.. test:: Conversion from GPS-coordinates to euclidian coordinates test
  :id: TEST_6
  :tags: unittest
  :status: passing

  A python class (CoordTests) with several tests:
  testing if euclidian x, y, z are converted correctly from GPS-coordinates,
  testing if the correct camera direction is returned.

.. needtable::
   :types: test
   :columns: title;status;incoming;tags
