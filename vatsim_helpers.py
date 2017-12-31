'''
Module contains helper functions for main.py for restful_vatsim
'''
import time, random, requests

################################################################################

def download():
    '''download() tries to download the latest vatsim data from a list of
    randomized servers to distribute server load'''
    #random urls to download from
    vatsim_urls = ["http://info.vroute.net/vatsim-data.txt", "http://data.vattastic.com/vatsim-data.txt", \
            "http://vatsim.aircharts.org/vatsim-data.txt", "http://vatsim-data.hardern.net/vatsim-data.txt", \
            "http://wazzup.flightoperationssystem.com/vatsim/vatsim-data.txt"]
    random_url = random.choice(vatsim_urls)
    #Download page
    try:
        data = requests.get(random_url).text
        if not(len(data)):
            print "Error in downloaded file"
            return None
        #Return data
        return data
    except:
        print "Error downloading data"
        return None

################################################################################

def check_line_validity(line):
    ''' check_line_validity() recieves an array of each line in the VATSIM raw
    data, wherein the array is the line already split by ":", and the function
    returns true if it's valid and false if it is not '''

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
        return {"Location": line[0], "IP Address": line[1], "Name": line[2],
        "Host Name": line[3], "Clients Allowed": line[4]}

    elif kwargs["type"] == "controllers":
        return {"Callsign": line[0], "Vatsim ID": line[1], \
        "Real Name": line[2], "Frequency": line[4], "Latitude": line[5], \
        "Longitude": line[6], "Visible Range": line[19], "ATIS": \
        line[35], "Login Time": line[37]}

    elif kwargs["type"] == "pilots":
        return {"Callsign": line[0], "Vatsim ID": line[1], "Real Name": line[2], \
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
        #Split by colon (the delimiter)
        vals = line.split(":")

        #Check if line is valid
        if not check_line_validity(vals):
            continue

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

class VatsimData():
    def __init__(self):
        #make a dummy file and update it
        self.latest_file = {'time_updated': 0, 'data': None}
        self.update_file()

    def update_file(self):
        '''update_file() checks for data freshness in the local cache and if
        data is too old, then it fetches new data. It then returns freshest data'''
        #Check cache freshness; call download if needed
        if (self.latest_file["time_updated"] + 120) < int(time.time()):
            #Needs updating
            new_file = download()
            if new_file is not None:
                self.latest_file["time_updated"] = int(time.time())
                #Jsonify the data
                self.latest_file["data"] = jsonify_data(new_file)
            else:
                print "Downloaded file not valid"

    def filter(self, value, **kwargs):
        # ------ TO--DO: add
        boiler_plate = {
            "voice_servers": "VOICE SERVERS contains a list of all running voice servers that clients can use",
            "pilots": "PILOTS contains information about all connected pilots",
            "controllers": "CONTROLLERS contains information about connected controllers"
        }

        curr_data = []

        #Loop through relevant data (pilots, controllers or voice servers)
        for item in self.latest_file["data"][value]:
            #Look at kwargs
            if "name" in kwargs["params"]:
                if "exactMatch" in kwargs["params"] and kwargs["params"]["name"] == item["Name"]:
                    curr_data.append(item)
                elif "exactMatch" not in kwargs["params"] and kwargs["params"]["name"] in item["Name"]:
                    curr_data.append(item)

            elif "name" not in kwargs["params"]:
                #No name supplied
                curr_data.append(item)

        #Deal with limit
        if "limit" in kwargs["params"]:
            return curr_data[:kwargs["params"]["limit"]]
        else:
            return curr_data

################################################################################

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
