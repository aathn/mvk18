.. req:: Capture video
   :id: req_01
   :tags: functional

   The camera shall capture mpeg video in 1280x720 with at least 15
   fps for at least 10 minutes continuously

.. req:: Stream video
   :id: req_2
   :tags: functional

   Our software shall send the captured video to an output URL / file
   continuously at a bit rate of 1000kb/s

.. req:: Send data to cloud
   :id: req_3
   :tags: functional

   The video data of streamed flights shall be sent to a cloud service provider

.. req:: Store video in cloud
   :id: req_4
   :tags: functional

   The video sent shall be stored in the cloud and organised in an
   SQL-database. The storage space not yet specified. (Måste
   specificera storage space)

.. req:: Display streams on Web page
   :id: req_5
   :tags: functional

   The web user shall be able to see all current streams on a Web page
   and the airplane numbers

.. req:: Display stored video on Web page
   :id: req_6
   :tags: functional

   The web user shall be able to see a list of previously recorded
   flights and filter after flight number

.. req:: Control the pan/tilt servo
   :id: req_7
   :tags: functional

   The servo shall take two input angles and move the camera to pan
   and tilt in those angles with a maximum difference of 5°

.. req:: Data parsing
   :id: req_8
   :tags: functional

   The Skysense shall parse (JSON) data from all flights into a format
   directly supported by the software

.. req:: Airplane selection
   :id: req_9
   :tags: functional

   The skysense shall automatically pick one airplane from the parsed
   data, prioritizing airplanes that are within a specified range
   (FYLL I NÄR VI VET)

.. req:: Translate GPS-position to relative position to the camera
   :id: req_10
   :tags: functional

   Our software shall be able to translate the GPS-position of
   airplanes to a position relative to the camera Unittesting

.. req:: Convert relative airplane position to camera pan/tilt angles
   :id: req_11
   :tags: functional

   The relative position shall be translated to camera pan/tilt angles
   instructing the camera where to point. This shall be achieved with
   a precision within 2°

.. req:: Selected airplane in view
   :id: req_12
   :tags: functional

   Our software should control the servo to keep the selected airplane
   fully in frame when possible.

.. req:: Keep movements smooth
   :id: req_13
   :tags: functional

   The servo position should be updated frequently enough to avoid
   jagged movement

.. req:: Predict flight path by extrapolating linearly
   :id: req_14
   :tags: functional

   As the airplane positions are provided in discrete chunks, the
   software needs to be able to predict flight paths to a certain
   extent.

.. req:: Avoid sun damage
   :id: req_15
   :tags: functional

   The camera shall never point directly towards the sun to avoid
   being damaged

.. req:: Automatically start streaming
   :id: req_16
   :tags: functional

   Automatically start video stream when there is a visible airplane
   in view

.. req:: Automatically stop streaming
   :id: req_17
   :tags: functional

   Automatically stop streaming when there no longer are any visible
   airplanes in view

.. req:: Configurable view
   :id: req_18
   :tags: functional

   The host shall be able to define the cameras view angle in a config
   file

.. req:: Abide view boundaries
   :id: req_19
   :tags: functional

   The camera shall not move outside of the hosts defined view angle

.. req:: Configuration process
   :id: req_20
   :tags: functional

   The user is able to set the direction the camera plattform is
   facing. Perhaps using the buttons on the skysense.

.. req:: Non-dependability on hardware
   :id: req_21
   :tags: functional

   To make it easier for FR24 to keep developing the project the
   software we write should be as indepedent on the specific hardware
   components as possible.

.. req:: Ensure that streaming is scalable
   :id: req_22
   :tags: functional
