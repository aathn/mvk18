==============
 REQUIREMENTS
==============
.. req:: Capture video
   :id: REQ_1
   :tags: functional
   :status: done
   :priority: 1

   The camera shall capture mpeg video in 1280x720 with at least 15
   fps for at least 10 minutes continuously

.. req:: Stream video
   :id: REQ_2
   :tags: functional
   :status: done
   :priority: 1

   Our software shall send the captured video to an output URL / file
   continuously at a bit rate of 1000kb/s

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

   The video sent shall be stored in the cloud and organised in an
   SQL-database. The storage space not yet specified. (Måste
   specificera storage space)

.. req:: Display streams on Web page
   :id: REQ_5
   :tags: functional
   :status: in progress
   :priority: 2

   The web user shall be able to see all current streams on a Web page
   and the airplane numbers

.. req:: Display stored video on Web page
   :id: REQ_6
   :tags: functional
   :status: backlog
   :priority: 3

   The web user shall be able to see a list of previously recorded
   flights and filter after flight number

.. req:: Control the pan/tilt servo
   :id: REQ_7
   :tags: functional
   :status: done
   :priority: 1

   The servo shall take two input angles and move the camera to pan
   and tilt in those angles with a maximum difference of 5°

.. req:: Data parsing
   :id: REQ_8
   :tags: functional
   :status: done
   :priority: 1

   The Skysense shall parse (JSON) data from all flights into a format
   directly supported by the software

.. req:: Airplane selection
   :id: REQ_9
   :tags: functional
   :status: in progress
   :priority: 1

   The skysense shall automatically pick one airplane from the parsed
   data, prioritizing airplanes that are within a specified range
   (FYLL I NÄR VI VET)

.. req:: Translate GPS-position to relative position to the camera
   :id: REQ_10
   :tags: functional
   :status: done
   :priority: 1

   Our software shall be able to translate the GPS-position of
   airplanes to a position relative to the camera Unittesting

.. req:: Convert relative airplane position to camera pan/tilt angles
   :id: REQ_11
   :tags: functional
   :status: done
   :priority: 1

   The relative position shall be translated to camera pan/tilt angles
   instructing the camera where to point. This shall be achieved with
   a precision within 2°

.. req:: Selected airplane in view
   :id: REQ_12
   :tags: functional
   :status: in progress
   :priority: 1

   Our software should control the servo to keep the selected airplane
   fully in frame when possible.

.. req:: Keep movements smooth
   :id: REQ_13
   :tags: functional
   :status: in progress
   :priority: 2

   The servo position should be updated frequently enough to avoid
   jagged movement

.. req:: Predict flight path by extrapolating
   :id: REQ_14
   :tags: functional
   :status: done
   :priority: 1

   As the airplane positions are provided in discrete chunks, the
   software needs to be able to predict flight paths to a certain
   extent.

.. req:: Avoid sun damage
   :id: REQ_15
   :tags: functional
   :status: backlog
   :priority: 2

   The camera shall never point directly towards the sun to avoid
   being damaged

.. req:: Automatically start streaming
   :id: REQ_16
   :tags: functional
   :status: done
   :priority: 1

   Automatically start video stream when there is a visible airplane
   in view

.. req:: Automatically stop streaming
   :id: REQ_17
   :tags: functional
   :status: done
   :priority: 1

   Automatically stop streaming when there no longer are any visible
   airplanes in view

.. req:: Configurable view
   :id: REQ_18
   :tags: functional
   :status: in progress
   :priority: 1

   The host shall be able to define the cameras view angle in a config
   file

.. req:: Abide view boundaries
   :id: REQ_19
   :tags: functional
   :status: done
   :priority: 1

   The camera shall not move outside of the hosts defined view angle

.. req:: Configuration process
   :id: REQ_20
   :tags: functional
   :status: in progress
   :priority: 2

   The user is able to set the direction the camera plattform is
   facing. Perhaps using the buttons on the skysense.

.. req:: Non-dependability on hardware
   :id: REQ_21
   :tags: functional
   :status: in progress
   :priority: 2

   To make it easier for FR24 to keep developing the project the
   software we write should be as indepedent on the specific hardware
   components as possible.

.. req:: Ensure that streaming is scalable
   :id: REQ_22
   :tags: functional
   :status: backlog
   :priority: 3

.. needtable::
   :tags: functional
   :style: datatable
   :sort_by: priority
   :columns: id;title;status;outgoing;priority
