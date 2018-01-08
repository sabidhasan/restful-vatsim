''' Docs '''
#Module imports
from flask import Flask, request
from flask_restful import Resource, Api
#For URL arguments
from webargs import fields, validate
from webargs.flaskparser import use_args, parser, abort
#Custom methods
from vatsim_classes import *

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
@app.route('/help/')
def hello():
    return '<strong>Here is the help</strong>'

class VoiceServers(Resource):
    ''' Route for /api/v1/VoiceServers[?params]. See docs for params usage '''

    #Define valid arguments
    args = {
        "name": fields.Str(required=False),
        "exactMatch": fields.Bool(required=False),
        "limit": fields.Int(required=False, validate=(lambda x: 1 <= x <= 50)),
        "forceUpdate": fields.Bool(required=False),
        "fields": fields.Str(required=False),
        "sort": fields.Str(required=False)
    }

    @use_args(args)
    def get(self, request_arguments):
        #force is the forceUpdate parameter (if provided by user in request arguments)
        force = request_arguments.get("forceUpdate", False)
        #Create voice server class, passing it forceUpdate
        vatsim_voice_server = VoiceServer(force_update=force)
        #Filter based on parameters
        return vatsim_voice_server.filter(params=request_arguments)

################################################################################
class Controllers(Resource):
    ''' Route for /api/v1/controllers/[?params]. See docs for params usage '''

    args = {
        "callsign": fields.Str(required=False),
        "real_name": fields.Str(required=False),
        "frequency": fields.Float(required=False),
        "min_latitude": fields.Float(required=False, validate=lambda x: -90 <= x <= 90),
        "max_latitude": fields.Float(required=False, validate=lambda x: -90 <= x <= 90),
        "min_longitude": fields.Float(required=False, validate=lambda x: -180 <= x <= 180),
        "max_longitude": fields.Float(required=False, validate=lambda x: -180 <= x <= 180),
        "airport": fields.Str(required=False, validate=lambda x: len(x) in [3, 4]),
        "in_atis": fields.Str(required=False),
        "min_visrange": fields.Int(required=False),
        "max_visrange": fields.Int(required=False),
        "min_logontime": fields.Str(required=False),
        "max_logontime": fields.Str(required=False),
        "limit": fields.Int(required=False, validate=(lambda x: 1 <= x <= 50)),
        "forceUpdate": fields.Bool(required=False),
        "sort": fields.Str(required=False),
        "fields": fields.Str(required=False)
    }

    @use_args(args)
    def get(self, request_arguments, cid=None):
         #force is the forceUpdate parameter (if provided by user in request arguments)
         force = request_arguments.get("forceUpdate", False)
         #Create pilot class, passing it url, cid and forceUpdate
         vatsim_controllers = Controller(request.url_rule, cid, force_update=force)

         return vatsim_controllers.filter(params=request_arguments)

################################################################################

class Pilots(Resource):
    ''' Route for /api/v1/pilots/[?params]. See docs for params usage '''

    #Define valid arguments
    args = {
        "fields": fields.Str(required=False),
        "callsign": fields.Str(required=False),
        "real_name": fields.Str(required=False),
        "min_latitude": fields.Float(required=False, validate=lambda x: -90 <= x <= 90),
        "max_latitude": fields.Float(required=False, validate=lambda x: -90 <= x <= 90),
        "min_longitude": fields.Float(required=False, validate=lambda x: -180 <= x <= 180),
        "max_longitude": fields.Float(required=False, validate=lambda x: -180 <= x <= 180),
        #String because you can type "FL350"
        "min_altitude": fields.Str(required=False),
        "max_altitude": fields.Str(required=False),
        "min_speed": fields.Int(required=False),
        "max_speed": fields.Int(required=False),
        "min_heading": fields.Int(required=False),
        "max_heading": fields.Int(required=False),
        "dep_airport": fields.Str(required=False),
        "arr_airport": fields.Str(required=False),
        "in_route": fields.Str(required=False),
        "min_logontime": fields.Str(required=False),
        "max_logontime": fields.Str(required=False),
        "aircraft": fields.Str(required=False),
        "limit": fields.Int(required=False, validate=(lambda x: 1 <= x <= 50)),
        "forceUpdate": fields.Bool(required=False),
        "sort": fields.Str(required=False)
    }

    @use_args(args)
    def get(self, request_arguments, cid=None):
         #force is the forceUpdate parameter (if provided by user in request arguments)
         force = request_arguments.get("forceUpdate", False)
         #Create pilot class, passing it url, cid and forceUpdate
         vatsim_pilots = Pilot(request.url_rule, cid, force_update=force)

         return vatsim_pilots.filter(params=request_arguments)

################################################################################

#add resources for relavant API paths. Get path list from respective classes
api.add_resource(VoiceServers, *VoiceServer().paths)
api.add_resource(Pilots, *Pilot().paths)
api.add_resource(Controllers, *Controller().paths)

################################################################################

@parser.error_handler
def handle_request_parsing_error(err):
    '''webargs error handler that uses Flask-RESTful's abort function to return
    a JSON error response to the client.'''
    errors = {
        "exactMatch": "The 'exactMatch' parameter must be a boolean (true/false). Invalid value supplied.",
        "limit": "The 'Limit' parameter must be a number from 1 to 50.",
        "name": "'Name' parameter must be string.",
        "forceUpdate": "'forceUpdate' parameter must be True or False",
        "max_latitude": "'max_latitude' parameter must be from -90 to +90",
        "min_latitude": "'min_latitude' parameter must be from -90 to +90",
        "max_longitude": "'max_longitude' parameter must be from -180 to +180",
        "min_longitude": "'min_longitude' parameter must be from -180 to +180",
        "min_heading": "'min_heading' must be numeric",
        "max_heading": "'max_heading' must be numeric",
        "min_speed": "'min_speed' must be a number",
        "max_speed": "'max_speed' must be a number",
        "frequency": "'frequency' must be numeric",
        "min_visrange": "'min_visrange' must be numeric",
        "max_visrange": "'max_visrange' must be numeric",
        "airport": "'airport' must be 3 or 4 digit ICAO/IATA code"
    }

    #Customize errors and abort request
    current_error = {"*" + error + "* Parameter": errors[error] for error in err[0]}
    abort(422, errors=current_error)

################################################################################

if __name__ == '__main__':
    app.run(debug=True)
