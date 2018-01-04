'''
Module contains helper functions for main.py for restful_vatsim
'''
import time, random, requests, os

################################################################################

def download():
    '''download() tries to download the latest vatsim data from a list of
    randomized servers to distribute server load'''

    #list of sources to download from
    vatsim_urls = ["http://info.vroute.net/vatsim-data.txt", "http://data.vattastic.com/vatsim-data.txt", \
            "http://vatsim.aircharts.org/vatsim-data.txt", "http://vatsim-data.hardern.net/vatsim-data.txt", \
            "http://wazzup.flightoperationssystem.com/vatsim/vatsim-data.txt"]
    random_url = random.choice(vatsim_urls)
    #Download page and save it to disk
    try:
        data = requests.get(random_url).text.encode('utf-8')
        if not(len(data)):
            raise ValueError
    except:
        print "Could not download file"
        return None

    with open("vatsim_data.txt", 'wb') as f:
        f.write(data)
    return data

################################################################################

def check_line_validity(line):
    ''' check_line_validity() recieves a line in the VATSIM raw data and the
	function returns true if it's valid and false if it is not '''

    line = line.split(":")
    try:
        #Check for VATSIM comments; these are not valid. First character of first
        #position in array
        if line[0][0] == ';':
            return False
        #This is an invalid line (non-pilot/ATC/voice server)
        if len(line) != 6 and len(line) != 42:
            return False
    #Line is not accessible at 0th position, so must be empty
    except IndexError:
        return False

    #Line must be valid
    return True

################################################################################

def prettify_data(line, **kwargs):
    ''' prettify_data() recieves a line of data from the vatsim file, already split,
    and prettifies it to make it ready for jsonifying - discards unneeded data, while
    keeping the data that the API needs to include. Returns a dictionary. Type =
    "pilot", "controller" or "voice_servers" '''

    if kwargs["type"] == "voice_servers":
        return {"Location": line[1], "Address": line[0], "Name": line[2],
        "Host Name": line[3], "Clients Allowed": line[4]}
    elif kwargs["type"] == "controllers":
        return {"Callsign": line[0], "Vatsim ID": int(line[1]), \
        "Real Name": line[2], "Frequency": line[4], "Latitude": line[5], \
        "Longitude": line[6], "Visible Range": line[19], "ATIS": \
        line[35], "Login Time": line[37]}
    elif kwargs["type"] == "pilots":
        return {"Callsign": line[0], "Vatsim ID": int(line[1]), "Real Name": line[2], \
        "Latitude": line[5], "Longitude": line[6], "Login Time": line[37], \
        "Altitude": line[7], "Ground Speed": line[8], "Heading": line[38], \
        "Route": line[30], "Remarks": line[29], "Planned Aircraft": line[9], \
        "Planned Departure Airport": line[11], "Planned Altitude": flightlevel_to_feet(line[12]), \
        "Planned Destination Airport": line[13], "Flight Type": line[21], "Planned Departure Time": \
        line[22]}

################################################################################

def jsonify_data(data):
    ''' jsonify_data() makes recieved raw VATSIM.txt data usable by trimming the
    fat, parsing for errors, and making data easily searchable '''

    #Linted data that will be returned
    parsed_data = {
        "pilots": [],
        "voice_servers": [],
        "controllers": []
    }
    #Loop through line by line
    for line in data.split("\n"):
		#Check if line is valid
        if not check_line_validity(line):
            continue
		#Split by colon (the delimiter)
        vals = line.split(":")
        #This is a voiceserver
        if len(vals) == 6:
            # Construct dictionary of this line + append to parsed data
            curr_data = prettify_data(vals, type="voice_servers")
            parsed_data["voice_servers"].append(curr_data)
        #ATC found
        elif vals[3] == "ATC":
            #Construct dictionary of this line, and append to parsed data
            curr_data = prettify_data(vals, type="controllers")
            parsed_data["controllers"].append(curr_data)
        #pilot found
        elif vals[3] == "PILOT":
            #Construct dictionary of this line
            curr_data = prettify_data(vals, type="pilots")
            parsed_data["pilots"].append(curr_data)
    return parsed_data

################################################################################

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

        try:
    		#Check cache freshness - call download if needed (or if forced update is true)
            if (self.latest_file["time_updated"] + 120) < int(time.time()) or kwargs["force_update"]:
    	        #Update the file
    	        self.update_file()
        except KeyError:
            #No force update parameter was provided, but we can assume it's false
            pass

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

    def filter(self, **kwargs):
        ''' Filters the data-set based on kwargs (see docs for kwarg help) '''

        curr_data = [{
            "Time Updated (UTC)": int(self.latest_file["time_updated"]),
            "Info": self.boiler_plate[self.verbose_name]
        }]
        #Loop through relevant data (pilots, controllers or voice servers)
        for item in self.latest_data[self.verbose_name]:
            #Look at kwargs
            if "name" in kwargs["params"]:
                if "exactMatch" in kwargs["params"] and kwargs["params"]["name"] == item["Name"]:
                    curr_data.append(item)
                elif "exactMatch" not in kwargs["params"] and kwargs["params"]["name"] in item["Name"]:
                    curr_data.append(item)

            elif "name" not in kwargs["params"]:
                #No name supplied
                curr_data.append(item)
        #Deal with limit. We use +1 because the first object is always info
        #about the file
        if "limit" in kwargs["params"]:
            curr_data[0]["Number of Records"] = kwargs["params"]["limit"]
            return curr_data[:kwargs["params"]["limit"]+1]
        else:
            curr_data[0]["Number of Records"] = len(curr_data) - 1
            return curr_data

################################################################################

class Pilot(VatsimData, object):
    ''' Use this class for accessing pilot data '''

    def __init__(self, page_url="", cid=None, **kwargs):
        super(Pilot, self).__init__(**kwargs)
        #For accessing boiler_plate text, etc.
        self.verbose_name = "pilots"
        #Generate base URL (stripping the constant portion) - root path from
        #parent class
        static_url = self.root_path + self.verbose_name + "/"
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

        self.basic_filtration_parameters = {
            "rating": instrument_rating,
            "cid": cid
        }

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

    #Comparator functions for filter method
    def compare(self, local_data_value, user_requested_value, comparator_function):
        ''' Called as comparator function - if user requested value is substring
        of the local_data_value then there is a match '''

        #Comparison looks at local line and applies a comparator function
        #to compare it to user requested parameter. "in" keyword requires a
        #custom within function, because it's a keyword not a first order function\
        try:
            local_data_value = float(local_data_value)
            user_requested_value = float(user_requested_value)
        except ValueError:
            pass

        if comparator_function(local_data_value, user_requested_value) == user_requested_value:
            return True
        return False

    def within(self, local_data_value, user_requested_value):
         ''' within() is a make-do first order function for the in keyword '''

         if user_requested_value in local_data_value:
            return user_requested_value
         return local_data_value

    def filter(self, **kwargs):
        ''' Filters the data-set based on kwargs (see docs for kwarg help) '''

        curr_data = [{
            "Time Updated (UTC)": int(self.latest_file["time_updated"]),
            "Info": self.boiler_plate[self.verbose_name]
        }]

        #return self.latest_file["data"][self.verbose_name]
        # #Loop through relevant data (pilots, controllers or voice servers)
        for item in self.latest_data[self.verbose_name]:
            #Whether to include the item
            include = False

            #Match type (ifr, vfr, alltypes)
            if (not self.basic_filtration_parameters["rating"]) or self.basic_filtration_parameters["rating"] == item["Flight Type"]:
                include = True

            #Match CID
            if item["Vatsim ID"] == self.basic_filtration_parameters["cid"] and include:
                #found exact CID, so must redefine the list with only this item
                curr_data = [curr_data[0]] + [item]
                break

            # if not include:
            #     #We have excluded based on basic parameters, so filter will fail
            #     continue

            #Run custom Filters
            api_names_to_local_data = {
                "callsign": {"db_name": "Callsign", "comparator": self.within},
                "realname": {"db_name": "Real Name", "comparator": self.within},
                "dep_airport": {"db_name": "Planned Departure Airport", "comparator": self.within},
                "arr_airport": {"db_name": "Planned Destination Airport", "comparator": self.within},
                "in_route": {"db_name": "Route", "comparator": self.within},
                "aircraft": {"db_name": "Planned Aircraft", "comparator": self.within},

                "min_latitude": {"db_name": "Latitude", "comparator": max},
                "max_latitude": {"db_name": "Latitude", "comparator": min},
                "min_longitude":  {"db_name": "Longitude", "comparator": max},
                "max_longitude":  {"db_name": "Longitude", "comparator": min},
                "min_speed": {"db_name": "Ground Speed", "comparator": max},
                "max_speed": {"db_name": "Ground Speed", "comparator": min},
                "min_altitude": {"db_name": "Altitude", "comparator": max},
                "max_altitude": {"db_name": "Altitude", "comparator": min},
                "min_heading": {"db_name": "Heading", "comparator": max},
                "max_heading": {"db_name": "Heading", "comparator": min}
            }

            #These must match by the end. If not, then this current line doesnt match
            requested_values = 0
            matched_values = 0
            #Compare all possible filter keywords
            for filter_param in api_names_to_local_data:
                if filter_param in kwargs["params"]:
                    #This parameter is requested, so update requested variable
                    requested_values += 1

                    try:
                        #If string, then remove quotation marks
                        user_requested_value = kwargs["params"][filter_param].replace("\"", "").replace("'", "")
                    except AttributeError:
                        #This is a non-string (likely float), so keep as is
                        user_requested_value = kwargs["params"][filter_param]
                    #Name for key in the local database
                    db_name = api_names_to_local_data[filter_param]["db_name"]
                    #The comparator function used to compare these
                    comparator_function = api_names_to_local_data[filter_param]["comparator"]

                    if self.compare(item[db_name], user_requested_value, comparator_function):
                        #This matches!! So let's add one to matched values
                        matched_values += 1
            if item["Callsign"] == 'AAL106':
                0/0
            #Loop is done, if values match and we hadnt excluded previously
            if requested_values == matched_values and include:
                include = True
            elif requested_values != matched_values:
                include = False
            #time
                # Login Time        min_logontime
                # Login Time        max_logontime
            #/api/v1/pilots/alltypes/?="now-5h4m"                             relative time (use h, m)
            #/api/v1/pilots/alltypes/?max_logontime="38947389473"                           unix time

            if include:
                #TO--DO: look at fields   #/api/v1/pilots/alltypes/?fields=groundspeed,heading                  only return specific fields

                # curr_data.append({"Txt": item["Vatsim ID"], "user": self.basic_filtration_parameters["cid"]})
                curr_data.append(item)



        #about the file
        if "limit" in kwargs["params"]:
            curr_data[0]["Number of Records"] = kwargs["params"]["limit"]
            return curr_data[:kwargs["params"]["limit"] + 1]
        else:
            curr_data[0]["Number of Records"] = len(curr_data) - 1
            return curr_data


def flightlevel_to_feet(flightlevel):
    '''The flightlevel_to_feet() function recieves something like 'FL360' or 1500
    and returns 36000 or 1500 '''

    #No altitude specified, so assume it is 0
    if not(flightlevel):
        return 0
    flightlevel = str(flightlevel).lower()
    if "fl" in flightlevel or "f" in flightlevel:
        #Sometimes, pilots put "VFR" for altitude, so this code will execute, but
        #Altitude is still not valid, so value error will occur
        try:
            return int(flightlevel.replace("fl", "").replace("f", "")) * 100
        except ValueError:
            return 0
    else:
        #It could be that a number was specified (so no flight level but thousands
        #of feet). If so, try to return it
        try:
            return int(flightlevel)
        except ValueError:
            return 0
