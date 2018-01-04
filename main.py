''' Docs '''
#PILOTS (client type is pilot)
    

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

#Module imports
from flask import Flask, request
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
####### filter data needs to learn hwo to filter pilot, controllers
####### class pilots and controllers for their "routes" in flask
####### make class for latest file, rather than object
####### jsonify data reads data from pilots and contorllers too
#######


################################################################################

class VoiceServers(Resource):
    ''' Route for /api/v1/VoiceServers[?params]. See docs for params usage '''

    #Define valid arguments
    args = {
        "name": fields.Str(required=False),
        "exactMatch": fields.Bool(required=False),
        "limit": fields.Int(required=False, validate=(lambda x: 1 <= x <= 50)),
        #forceUpdate forces a download of a new file
        "forceUpdate": fields.Bool(required=False)
    }

    @use_args(args)
    def get(self, request_arguments):
        #force is the forceUpdate parameter (if provided by user in request arguments)
        force = request_arguments["forceUpdate"] if "forceUpdate" in request_arguments else False
        #Create voice server class, passing it forceUpdate
        vatsim_voice_server = VoiceServer(force_update=force)
        #Filter based on parameters
        return vatsim_voice_server.filter(params=request_arguments)

################################################################################

class Pilots(Resource):
    ''' Route for /api/v1/Pilots/[?params]. See docs for params usage '''

    #Define valid arguments
    args = {
        "fields": fields.Str(required=False),
        "callsign": fields.Str(required=False),
        "real_name": fields.Str(required=False),
        "min_latitude": fields.Float(required=False),
        "max_latitude": fields.Float(required=False),
        "min_longitude": fields.Float(required=False),
        "max_longitude": fields.Float(required=False),
        "min_altitude": fields.Int(required=False),
        "max_altitude": fields.Int(required=False),
        "min_speed": fields.Int(required=False),
        "max_speed": fields.Int(required=False),
        "min_heading": fields.Int(required=False),
        "max_heading": fields.Int(required=False),
        "dep_airport": fields.Str(required=False),
        "arr_airport": fields.Str(required=False),
        "in_route": fields.Str(required=False),
        "logon_time": fields.Int(required=False),
        "limit": fields.Int(required=False, validate=(lambda x: 1 <= x <= 50)),
        #forceUpdate forces a download of a new file
        "forceUpdate": fields.Bool(required=False)
    }

    @use_args(args)
    def get(self, request_arguments, cid=None):
         #force is the forceUpdate parameter (if provided by user in request arguments)
         force = request_arguments["forceUpdate"] if "forceUpdate" in request_arguments else False
         #Create pilot class, passing it url, cid and forceUpdate
         vatsim_pilots = Pilot(request.url_rule, cid, force_update=force)

         return vatsim_pilots.filter(params=request_arguments)

# No 2nd one?        make it "alltypes"
# 2nd one Num        make it "alltypes" and append the Number
# 2nd one alltypes   check for third one (number), and then filters
# 2nd one VFR        filter by VFR then check for third one (number), and then filters
# 2nd one IFR        filter by IFR then check for third one (number), and then filters
#
#                                 /pilots/IFR/?-----
#                                 /pilots/IFR/50000/?----
#
#                                 /pilots/VFR/?----
#                                 /pilots/VFR/50000/?----
#
#                                 /pilots/alltypes/?----
#                                 /pilots/alltypes/50000/?----
#
#                                 /pilots/?----
#                                 /pilots/50000/?----



################################################################################

#add resources for relavant API paths. Get path list from respective classes
api.add_resource(VoiceServers, *VoiceServer().paths)
api.add_resource(Pilots, *Pilot().paths)



################################################################################

@parser.error_handler
def handle_request_parsing_error(err):#
    '''webargs error handler that uses Flask-RESTful's abort function to return
    a JSON error response to the client.'''
    errors = {
        "exactMatch": "The 'exactMatch' parameter must be a boolean (true/false). Invalid value supplied.",
        "limit": "The 'Limit' parameter must be a number from 1 to 50.",
        "name": "'Name' parameter must be string.",
        "forceUpdate": "'forceUpdate' parameter must be True or False"
    }

    #Customize errors and abort request
    current_error = {"*" + error + "* Parameter": errors[error] for error in err[0]}
    abort(422, errors=current_error)

################################################################################

if __name__ == '__main__':
    app.run(debug=True)
