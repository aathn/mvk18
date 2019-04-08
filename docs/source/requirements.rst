==============
 REQUIREMENTS
==============
.. req:: Capture video
   :id: REQ_1
   :tags: functional
   :status: done
   :links: TEST_2
   :priority: 1

   The software shall be capable of receiving continuous video output from a camera.

.. req:: Captured video quality
   :links: REQ_1
   :tags: quality

   The software should be able to handle a video stream of 1280x720
   mpeg video with at least 15 fps for at least 10 minutes
   continuously.

.. req:: Stream video
   :id: REQ_2
   :tags: functional
   :status: done
   :links: TEST_2
   :priority: 1

   Our software shall send the captured video to an output URL / file.

.. req:: Streamed video quality
   :links: REQ_2
   :tags: quality

   The software should be able to output the video
   stream received from the camera continuously at a bit rate of
   1000kb/s

.. req:: Send data to cloud
   :id: REQ_3
   :tags: functional
   :status: backlog
   :priority: 2

   The video data of streamed flights shall be sent to a cloud service provider

.. req:: Store video in cloud
   :id: REQ_4
   :tags: functional
   :status: backlog
   :priority: 3

   The video sent shall be stored in the cloud and organised in a
   database.

.. req:: Display streams on web page
   :id: REQ_5
   :tags: functional
   :status: in progress
   :priority: 2

   The web user shall be able to see all current streams on a web page
   along with relevant information.

.. req:: Display stored video on web page
   :id: REQ_6
   :tags: functional
   :status: backlog
   :priority: 3

   The web user shall be able to see a list of previously recorded
   flights on a web page.

.. req:: Filter among previous recordings
   :id: REQ_21
   :tags: functional
   :status: backlog
   :priority: 4

   The web user shall be able to filter previous recordings after
   flight number and other information.

.. req:: Control the pan/tilt servo
   :id: REQ_7
   :tags: functional
   :status: done
   :links: TEST_1
   :priority: 1

   The servo shall take two input angles and move the camera to pan
   and tilt in those angles.

.. req:: Pan/tilt servo accuracy
   :tags: quality
   :links: REQ_7

   The pan/tilt servo should be calibrated in such a way that the
   difference between input angles and output angles is not greater
   than 0.05 radians

.. req:: Data parsing
   :id: REQ_8
   :tags: functional
   :status: done
   :links: TEST_3
   :priority: 1

   The Skysense shall parse (JSON) data from all flights into a format
   directly supported by the software

.. req:: Airplane selection
   :id: REQ_9
   :tags: functional
   :status: in progress
   :priority: 1

   The skysense shall automatically pick one airplane from the parsed
   data

.. req:: Airplane selection criterions
   :links: REQ_9
   :tags: quality

   The software shall prioritize airplanes that are within 40,000 feet
   (~12 km), and avoid filming airplanes that are flying away from the
   camera

.. req:: Translate GPS-position to relative position to the camera
   :id: REQ_10
   :tags: functional
   :status: done
   :priority: 1

   Our software shall be able to translate the GPS-position of
   airplanes to a position relative to the camera using a horizontal coordinate
   system

.. req:: Convert relative airplane position to camera pan/tilt angles
   :id: REQ_11
   :tags: functional
   :status: done
   :priority: 1

   The relative position shall be translated to camera pan/tilt angles
   instructing the camera where to point.

.. req:: Conversion accuracy
   :links: REQ_11
   :tags: quality

   The conversion of relative position to pan/tilt angle shall be
   achieved with a precision within 0.05 radians.

.. req:: Selected airplane in view
   :id: REQ_12
   :tags: functional
   :status: in progress
   :priority: 1

   Our software should control the servo to keep the selected airplane
   in the frame of view when possible

.. req:: Airplane tracking quality
   :id: QUAL_1
   :links: REQ_12
   :tags: quality

   The servo position should be updated frequently enough to avoid
   jagged movement. It should also keep the airplane centered in the
   field of view.

.. req:: Predict flight path by extrapolating
   :id: REQ_13
   :tags: functional
   :status: done
   :priority: 1

   The software shall to be able to predict flight paths to make up
   for any lack of continuity in the received data.

.. req:: Extrapolation accuracy
   :links: REQ_13
   :tags: quality

   The extrapolation should be accurate for airplanes following a
   linear trajectory. That is, requirement :need:`QUAL_1` should be
   fulfilled for an airplane following such a trajectory even when new
   data is not being received continuously.

.. req:: Avoid sun damage
   :id: REQ_14
   :tags: functional
   :status: backlog
   :priority: 2

   The camera shall never point directly towards the sun to avoid
   being damaged.

.. req:: Automatically start streaming
   :id: REQ_15
   :tags: functional
   :status: done
   :priority: 1

   The software should automatically start a video stream when there
   is a visible airplane in view.

.. req:: Automatically stop streaming
   :id: REQ_16
   :tags: functional
   :status: done
   :priority: 1

   The software should automatically stop streaming when there no
   longer are any visible airplanes in view.

.. req:: Configurable view
   :id: REQ_17
   :tags: functional
   :status: in progress
   :priority: 1

   The host shall be able to define the camera's view angle, to enable
   the camera to only track visible airplanes.

.. req:: Abide view boundaries
   :id: REQ_18
   :tags: functional
   :status: done
   :priority: 1

   The camera shall not move outside of the host's defined view angle.

.. req:: Configuration process
   :id: REQ_19
   :tags: functional
   :status: in progress
   :priority: 2

   The host shall be able to set the direction and view angle of the
   camera using a configuration file.

.. req:: Non-dependability on hardware
   :id: QUAL_2
   :tags: quality

   To make it easier for Flightradar24 to keep developing after the
   course is finished, the software should be as indepedent on the
   specific hardware components as possible.

.. req:: Ensure that streaming is scalable
   :id: QUAL_3
   :tags: quality

   The streaming setup should be scalable in order to able to keep up
   with a growing number of viewers.

.. needtable::
   :tags: functional
   :style: datatable
   :sort_by: priority
   :columns: id;title;status;outgoing;incoming;priority
