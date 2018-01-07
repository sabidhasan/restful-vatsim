'''Module contains classes for main.py used by restful_vatsim'''
#import standard libraries
import os, time
#import non-class functions
from vatsim_functions import *

#Class structure. Starred classes should be created directly
# VatsimData
# |
#  -->   *VoiceServer            HumanUser
#                                   |
#                                    -->   *Pilot        *Controller

class VatsimData(object):
    ''' Generic base class for voiceServer, pilots and controllers '''
    #Boiler plate text that will get added to returned objects
    boiler_plate = {
        "voice_servers": "VOICE SERVERS contains a list of running voice servers that clients can use",
        "pilots": "PILOTS contains information about connected pilots",
        "controllers": "CONTROLLERS contains information about connected controllers"
    }
    #Path to local cache file
    file_path = "vatsim_data.txt"
    #constant path
    root_path = "/api/v1/"

    def __init__(self, **kwargs):
        #stores latest file dictionary that has file data and time updated
        #Get latest cached file, which returns latest saved file
        #on disk. If none exists, it returns a dummy
        self.latest_file = self.latest_cached_file()

		#Check cache freshness - call download if needed (or if forced update is true)
        if (self.latest_file.get("time_updated", 0) + 120) < int(time.time()) or kwargs.get("force_update"):
	        #Update the file
	        self.update_file()

    @property
    def latest_data(self):
        #Property to return latest file's data
        try:
            return self.latest_file["data"]
        #The latest file must not be defined yet
        except KeyError:
            return None

    def latest_cached_file(self):
        ''' latest_cached_file() returns the latest file available on disk
        or returns a dummy blank file with time_updated of 0. '''

        #See if file exists
        if not os.path.isfile(self.file_path):
            return {'time_updated': 0, 'data': None}
        else:
            #Return file from disk
            with open(self.file_path) as f:
                data = jsonify_data(f.read())
                self.latest_file = {'time_updated': os.path.getmtime(self.file_path), 'data': data}
        return self.latest_file

    def update_file(self):
        '''update_file() fetches new data. It then returns freshest data'''
        #Needs updating
        new_file = download()

        if new_file is not None:
            self.latest_file["time_updated"] = int(time.time())
            #Jsonify the data
            self.latest_file["data"] = jsonify_data(new_file)
        else:
            print "Downloaded file not valid"

################################################################################

class VoiceServer(VatsimData, object):
    ''' Use this class for accessing Voice Server data '''
    def __init__(self, **kwargs):
        super(VoiceServer, self).__init__(**kwargs)
        self.verbose_name = "voice_servers"
        self.paths = [self.root_path + self.verbose_name]

        self.strip_fields_dict = {"location": "Location", "address": "Address", "name": "Name", \
            "host_name": "Host Name", "clients_allowed": "Clients Allowed"}

    def filter(self, **kwargs):
        ''' Filters the data-set based on kwargs (see docs for kwarg help) '''
        #Start variable
        curr_data = []

        #Loop through relevant data (pilots, controllers or voice servers)
        for item in self.latest_data[self.verbose_name]:
            include = False
            #Look at kwargs
            if "name" in kwargs["params"]:
                if "exactMatch" in kwargs["params"] and kwargs["params"]["name"] == item["Name"]:
                    include = True
                elif "exactMatch" not in kwargs["params"] and kwargs["params"]["name"] in item["Name"]:
                    include = True
            else:
                #No name supplied
                include = True
            if include:
                #Filter by view, culling unneeded fields, while keeping VATSIM ID
                try:
                    user_requested_fields = filter(None, kwargs["params"]["fields"].split(","))
                except:
                    #No field supplied (no "fields" in params)
                    user_requested_fields = ""
                #Get requested fields
                required_fields = strip_fields(item, self.verbose_name, self.strip_fields_dict, user_requested_fields)
                curr_data.append(required_fields)
        #Sort if needed
        curr_data = sort_on_field(curr_data, kwargs["params"].get("sort"), self.strip_fields_dict)
        #Add boiler plate
        curr_data = add_boiler_plate(curr_data, self.latest_file["time_updated"], self.boiler_plate[self.verbose_name])
        #Cut by index
        end_index = (kwargs["params"]["limit"] + 1) if "limit" in kwargs["params"] else None
        return curr_data[:end_index]

################################################################################

class HumanUser(VatsimData, object):
    ''' Base class for Pilots and Controllers, because a lot of code in the __init__
    method is repeated for those two classes '''

    def __init__(self, verbose_name, page_url="", cid=None, **kwargs):
        super(HumanUser, self).__init__(**kwargs)

        #Generate base URL (stripping the constant portion) - root path from
        #parent class
        static_url = self.root_path + verbose_name + "/"
        #Get base URL by stripping the static URL
        self.base_url = str(page_url).replace(static_url, "")

        #Basic filtration parameters to help filtration function with non-keyword
        #argument filters (these are hard coded into URL)
        try:
            if self.base_url.split("/")[0] == "alltypes":
                #This is really a custom type, so make it "unknown"
                raise IndexError
            #first letter should be the flight code ("IFR" => "I" or "VFR -> "V")
            instrument_rating = self.base_url.split("/")[0][0]
        except IndexError:
            instrument_rating = ""

        #Hard coded parameters in URL
        self.basic_filtration_parameters = {
            "rating": instrument_rating,
            "cid": cid
        }

class Controller(VatsimData, object):
     pass
#     ''' Use this class for accessing controller data '''
#
#             self.strip_fields_dict = {"callsign": "Callsign", "vatsim_id": "Vatsim ID", "real_name": "Real Name", \
        #         "frequency": "Frequency", "latitude": "Latitude", "longitude": "Longitude", \
        #         "visible_range": "Visible Range", "atis": "ATIS", "login_time": "Login Time"}


class Pilot(HumanUser, object):
    ''' Use this class for accessing pilot data '''
    def __init__(self, page_url="", cid=None, **kwargs):
        #For accessing boiler_plate text, etc.
        self.verbose_name = "pilots"

        super(Pilot, self).__init__(self.verbose_name, page_url, cid, **kwargs)

        #Paths for routing accessible for flask restful
        self.paths = [
              self.root_path + self.verbose_name,
              self.root_path + self.verbose_name + '/alltypes',
              self.root_path + self.verbose_name + '/alltypes/<int:cid>',
              self.root_path + self.verbose_name + '/VFR',
              self.root_path + self.verbose_name + '/VFR/<int:cid>',
              self.root_path + self.verbose_name + '/IFR',
              self.root_path + self.verbose_name + '/IFR/<int:cid>'
        ]

        #Run custom Filters
        self.possible_parameters = {
            "callsign": {"clean_name": "Callsign", "comparator": within},
            "real_name": {"clean_name": "Real Name", "comparator": within},
            "dep_airport": {"clean_name": "Planned Departure Airport", "comparator": within},
            "arr_airport": {"clean_name": "Planned Destination Airport", "comparator": within},
            "in_route": {"clean_name": "Route", "comparator": within},
            "in_remarks": {"clean_name": "Remarks", "comparator": within},
            "aircraft": {"clean_name": "Planned Aircraft", "comparator": within},
            "min_latitude": {"clean_name": "Latitude", "comparator": maximum},
            "max_latitude": {"clean_name": "Latitude", "comparator": minimum},
            "min_longitude":  {"clean_name": "Longitude", "comparator": maximum},
            "max_longitude":  {"clean_name": "Longitude", "comparator": minimum},
            "min_speed": {"clean_name": "Ground Speed", "comparator": maximum},
            "max_speed": {"clean_name": "Ground Speed", "comparator": minimum},
            "min_altitude": {"clean_name": "Altitude", "comparator": maximum},
            "max_altitude": {"clean_name": "Altitude", "comparator": minimum},
            "min_heading": {"clean_name": "Heading", "comparator": maximum},
            "max_heading": {"clean_name": "Heading", "comparator": minimum},
            "min_logontime": {"clean_name": "Login Time", "comparator": maximum},
            "max_logontime": {"clean_name": "Login Time", "comparator": minimum}
        }

        self.strip_fields_dict = {"callsign": "Callsign", "vatsim_id": "Vatsim ID", "real_name": "Real Name", \
            "latitude": "Latitude", "longitude": "Longitude", "login_time": "Login Time", \
            "altitude": "Altitude", "ground_speed": "Ground Speed", "heading": "Heading", \
            "route": "Route", "remarks": "Remarks", "planned_aircraft": "Planned Aircraft", \
            "airport_destination": "Planned Destination Airport", "airport_origin": "Planned Departure Airport", \
            "planned_altitude": "Planned Altitude", "flight_type": "Flight Type", "time": "Planned Departure Time"}

    def filter(self, **kwargs):
        ''' Filters the data-set based on kwargs (see docs for kwarg help) '''
        curr_data = []

        # #Loop through relevant data (pilots, controllers or voice servers)
        for item in self.latest_data[self.verbose_name]:
            #Rating must match (if it doesnt exist then its alltypes)
            if self.basic_filtration_parameters["rating"] and self.basic_filtration_parameters["rating"] != item["Flight Type"]:
                continue
            #If CID supplied, then it must match, otherwise continue
            if self.basic_filtration_parameters["cid"] and self.basic_filtration_parameters["cid"] != item["Vatsim ID"]:
                continue

            #Applied to user inputs before filtration - altitude -> ft; time -> unix epoch time
            sanitation_functions = {
                "min_altitude": flightlevel_to_feet,
                "max_altitude": flightlevel_to_feet,
                "min_logontime": parseTime,
                "max_logontime": parseTime
            }

            #These must match by the end. If not, then this current line doesnt match
            requested_values, matched_values = (0, 0)

            #Compare all possible filter keywords - must loop thru self.possible_parameters
            #because kwargs[params] has a bunch of other crap (forceUpdate, etc.)
            for filter_param in self.possible_parameters:
                if filter_param in kwargs["params"]:
                    requested_values += 1
                    #If string, then remove quotation marks (if AttributeError then its a float)
                    try:
                        user_requested_value = kwargs["params"][filter_param].replace("\"", "").replace("'", "")
                    except AttributeError:
                        user_requested_value = kwargs["params"][filter_param]

                    #Sanitize input
                    if filter_param in sanitation_functions:
                        desanitizer = sanitation_functions[filter_param]
                        user_requested_value = desanitizer(user_requested_value)

                    #Name for key in the local database
                    clean_name = self.possible_parameters[filter_param]["clean_name"]
                    #The comparator function used to compare these
                    comparator_function = self.possible_parameters[filter_param]["comparator"]

                    if compare(item[clean_name], user_requested_value, comparator_function):
                        matched_values += 1

            #if some parameter failed, then it means it didnt match for this record
            if requested_values != matched_values: continue

            #Filter by fields, culling unneeded fields. If no field was specified, then make it""
            try:
                user_requested_fields = filter(None, kwargs["params"]["fields"].split(","))
            except:
                user_requested_fields = ""
            #Get requested fields
            required_fields = strip_fields(item, self.verbose_name, self.strip_fields_dict, user_requested_fields)
            curr_data.append(required_fields)
            #
            # #Sort if needed, TO--DO: eror is if you are not seeing a field and sorting on it, it doesnt work
            # try:
            #     curr_data.sort(key=lambda x: x[self.strip_fields_dict[kwargs["params"]["sort"]]])
            # except KeyError:
            #     pass

        #Sort if needed
        curr_data = sort_on_field(curr_data, kwargs["params"].get("sort"), self.strip_fields_dict)
        #Add boiler plate text
        curr_data = add_boiler_plate(curr_data, self.latest_file["time_updated"], self.boiler_plate[self.verbose_name])
        # Find end index for limit (if it's None, then it splices list until the end)
        end_index = (kwargs["params"]["limit"] + 1) if "limit" in kwargs["params"] else None
        return curr_data[:end_index]
