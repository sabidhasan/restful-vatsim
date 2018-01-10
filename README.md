# restful-vatsim

Serves data in RESTful format from VATSim flight simulation network. Supports clients, pilots and ATC; filtering by **almost** every possible criteria; local caching, to reduce load on Vatsim servers.

For usage see documentation - *docs.py*.

### Example

The API is currently hosted on [Heroku](http://restful-vatsim.herokuapp.com), but can be easily deployed locally or elsewhere.

### Libraries Required

- Python (written on 2.7)
- Flask (tested on 0.12.2)
- flask_restful
- requests (tested on 2.12.4)
- webargs (tested on 1.8.1)
- StringDist (tested on 1.0.9)
- gunicorn (can use Flask's testing server too)

### Installation

With the required libraries installed, you can run locally using

` python main.py `

For deploying on Heroku, use Procfile, requirements.txt and runtime.txt

### To Do

- logging of errors
- documentation/usage - docs.py
- field validation (things like sort should look for valid input using regex?)

### Uses

Some example uses for the API for an end user:

*  About to depart Aircraft (speed and altitude)
*  Busiest Airports
*  VirtualAirline searching (remarks)
*  Planes violating speed rules (<250 kts <18000 ft)
*  Planes heading a certain direction, in a certain location
*  Who just signed in and got going quickly
*  Find who is streaming on twitch ("twitch" in remarks)
*  Fastest planes currently online
