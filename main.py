#VOICE SERVER
    #/api/v1/voiceServers
    #/api/v1/voiceServers?name=London                                only servers with "london" as name
    #/api/v1/voiceServers?name=London&exactMatch=true                match exactly
    #/api/v1/voiceServers?limit=5                                    limit to 5

#PILOTS (client type is pilot)
    #/api/v1/pilots                                                  all pilots

    #/api/v1/pilots/IFR                                              all pilots who are IFR
    #/api/v1/pilots/VFR
    #/api/v1/pilots/alltypes                                              all VFR and IFR and other pilots

    #/api/v1/pilots/alltypes/50000                                        identify by CID



    #/api/v1/pilots/alltypes/?fields=groundspeed,heading                  only return specific fields

    #/api/v1/pilots/alltypes/?callsign="AA"                                    callsign contains "AA"
    #/api/v1/pilots/alltypes/?realname="Test"                                  identify by exact name

    #/api/v1/pilots/alltypes/?min_latitude=50&maxlatitude=100                   identify by latitude
    #/api/v1/pilots/alltypes/?min_longitude=50&maxlongitude=100                 identify by latitude
    #/api/v1/pilots/alltypes/?min_altitude=0&maxaltitude=FL100                  identify by altitude
    #/api/v1/pilots/alltypes/?min_speed=0&maxspeed=0
    #/api/v1/pilots/alltypes/?min_heading=0&maxheading=100

    #/api/v1/pilots/alltypes/?dep_airport="CYVR"
    #/api/v1/pilots/alltypes/?arr_airport="CYVR"
    #/api/v1/pilots/alltypes/?in_route="YVR"                                    route contains yvr

    #/api/v1/pilots/alltypes/?logontime<="now-5h4m"                             relative time (use h, m)
    #/api/v1/pilots/alltypes/?logontime>"38947389473"                           unix time

#CENTERS (client type is center)
    #/api/v1/controllers/                                               all atc

    #api/v1/controllers/centers                                         type center
    #api/v1/controllers/towers                                          type tower
    #api/v1/controllers/alltypes                                            type all of the above

    #api/v1/controllers/alltypes/50000                                       specific CID




    #/api/v1/controllers/alltypes/?fields=callsign,realname                       only return specific fields

    #/api/v1/controllers/alltypes/?callsign="EDDM"                                identify where callsign contains ...
    #/api/v1/controllers/alltypes/?realname="Edward"                              identify where name contains ...

    #/api/v1/controllers/alltypes/?min_latitude=50&maxlatitude=100                   identify by latitude
    #/api/v1/controllers/alltypes/?min_longitude=50&maxlongitude=100                 identify by latitude

    #/api/v1/controllers/alltypes/?frequency=124.95                                 identify by freq.

    #/api/v1/controllers/alltypes/?atis="military"                              ATIS text content

    #/api/v1/controllers/alltypes/?logontime<="now-5h4m"                             relative time (use h, m)
    #/api/v1/controllers/alltypes/?logontime>"38947389473"                           unix time

#return shoyld always have update time





#Module imports
from flask import Flask
from flask_restful import Resource, Api
#For URL arguments
from webargs import fields, validate
from webargs.flaskparser import use_args, parser, abort
#Custom methods
from vatsim_helpers import *

#create flask app
app = Flask(__name__)
api = Api(app)


#######TO--DO
####### filter data needs to learn hwo to filtervoice server, pilot, controllers
####### class pilots and controllers for their "routes" in flask
####### make class for latest file, rather than object
####### jsonify data reads data from pilots and contorllers too
#######

#Restful routes
class VoiceServers(Resource):
    #Build valid arguments dictionary
    args = {
        'name': fields.Str(required=False),
        'exactMatch': fields.Bool(required=False),
        'limit': fields.Int(required=False, validate=(lambda x: 1 <= x <= 50))
    }

    #def __init__(self):
#        super(VoiceServers, self).__init__()
#        self.full_name = "voice_servers"

    @use_args(args)
    def get(self, request_arguments):
        #Create class definition
        voice_server = voiceServer()

        #Filter based on parameters
        return_data = voice_server.filter(params=request_arguments)
        #filter_data(latest_file, filter="voice_servers", params=request_arguments)



        return return_data
        #Validate keyword arguments

        #Build complete list

        #Filter if needed

        #if name:
    #        return {'name': name, 'exactMatch': exactMatch, 'limit': limit}
#        else:
        #    return {'none': "none"}

        #Return list as found

api.add_resource(VoiceServers, '/api/v1/voiceServers')

@parser.error_handler
def handle_request_parsing_error(err):#
    '''webargs error handler that uses Flask-RESTful's abort function to return
    a JSON error response to the client.'''
    errors = {
        "exactMatch": "The 'exactMatch' parameter must be a boolean (true/false). Invalid value supplied.",
        "limit": "The 'Limit' parameter must be a number from 1 to 50.",
        "name": "'Name' parameter must be string."
    }

    #Customize errors and abort request
    current_error = {"*" + error + "* Parameter": errors[error] for error in err[0]}
    abort(422, errors=current_error)



if __name__ == '__main__':
    app.run(debug=True)
