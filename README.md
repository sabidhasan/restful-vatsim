# restful-vatsim

Serves RESTful data from VATSim flight simulation network
Used by VATSee on the backend.
For usage see documentation

### Libraries Required

- Flask (at least 0.12.2)
- flask_restful
- requests (at least 2.12.4)
- webargs (at least 1.8.1)
- StringDist (at least 1.0.9)

### Installation
-

### To Do
- logging
- documentation/usage
- help page (non API pages should redirect to friendly help page)
- field validation (things like sort should look for valid input using regex?)

### Uses
-  About to depart Aircraft (speed and altitude)
-  Busiest Airports
-  VirtualAirline searching (remarks)
-  Planes violating speed rules (<250 kts <18000 ft)
-  Planes heading a certain direction, in a certain location
-  Who just signed in and got going quickly
-  Find who is streaming on twitch ("twitch" in remarks)
-  Fastest planes currently online
