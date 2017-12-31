'''
Module contains helper functions for main.py for restful_vatsim
'''
import time, random, requests

def update_file(current_file):
    '''update_file() checks for data freshness in the local cache and if
    data is too old, then it fetches new data. It then returns freshest data'''
    #Check cache freshness; call download if needed
    if (current_file["time_updated"] + 120) < int(time.time()):
        #Needs updating
        new_file = download()
        if new_file is not None:
            current_file["time_updated"] = int(time.time())
            #Jsonify the data
            current_file["data"] = jsonify_data(new_file)
        else:
            print "Downloaded file not valid"

    #Return newest data
    return current_file

################################################################################
################################################################################
################################################################################

def download():
    '''download() tries to download the latest vatsim data from a list of
    randomized servers'''
    #random urls to download from
    vatsim_urls = ["http://info.vroute.net/vatsim-data.txt", "http://data.vattastic.com/vatsim-data.txt", \
            "http://vatsim.aircharts.org/vatsim-data.txt", "http://vatsim-data.hardern.net/vatsim-data.txt", \
            "http://wazzup.flightoperationssystem.com/vatsim/vatsim-data.txt"]
    random_url = random.choice(vatsim_urls)
    #Download page
    try:
        data = requests.get(random_url).text
        if not(len(data)):
            raise ConnectionError
    except:
        print "Error downloading data"
        return None
    #Return data
    return data

################################################################################
################################################################################
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
    #Line is not accessible at 0th position, so must be empty to being with
    except IndexError:
        return False

    return True

################################################################################
################################################################################
################################################################################

def jsonify_data(data):
    ''' jsonify_data() makes recieved raw VATSIM.txt data usable by trimming the
    fat, parsing for errors, and making data easily searchable '''

    #Linted data that will be returned
    parsed_data = {
        "pilots": ["PILOTS contains information about all connected pilots"],
        "voiceServers": ["VOICE SERVERS contains a list of all running voice servers that clients can use"],
        "controllers": ["CONTROLLERS contains information about connected controllers"]
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
            # Construct dictionary of this line
            curr_data = {"Location": vals[0], "IP Address": vals[1], "Name": vals[2],
            "Host Name": vals[3], "Clients Allowed": vals[4]}

            #Append to parsed data
            parsed_data["voiceServers"].append(curr_data)

        #ATC found
        elif vals[3] == "ATC":
            pass
        elif vals[3] == "PILOT":
            pass

        return parsed_data

        # if vals[3] == "ATC":
        #     try:
        #         inj = '''INSERT INTO 'onlines' ("callsign", "time_updated", "cid", "real_name", "frequency", "VATSIMlatitude", "VATSIMlongitude", "visible_range", "ATIS_msg", "time_logon", "type", "latest")''' + \
        #         ''' VALUES ("%s", "%s", "%s", "%s", "%s", %s, %s, %s, "%s", "%s", "%s", "%s")''' % (vals[0], str(int(time.time())), vals[1], vals[2], vals[4] , float(vals[5]), float(vals[6]), int(vals[19]), \
        #         vals[35].replace("\"", "").replace("'", ""), str(vals[37]), vals[3], "1")
        #         c.execute(inj)
        #         counter += 1
        #     except:
        #         #TO--DO Log the error here
        #         print("Error", vals[0:7], ". . .")
        #         continue
        #
        # elif vals[3] == "PILOT":
        #     try:
        #         inj = '''INSERT INTO "onlines" ("callsign", "time_updated", "cid", "real_name", "VATSIMlatitude", "VATSIMlongitude", "time_logon", "type", "altitude", "groundspeed"''' + \
        #         ''', "planned_aircraft", "planned_tascruise", "planned_depairport", "planned_altitude", "planned_destairport", "planned_flighttype", "planned_deptime", "planned_altairport"''' + \
        #         ''', "planned_remarks", "planned_route", "heading", "latest") VALUES ("%s", "%s", "%s", "%s", %s, %s, "%s", "%s", %s, %s, "%s", "%s", "%s", %s, "%s", "%s", "%s", "%s", "%s", "%s", %s, %s)''' % \
        #         (vals[0], str(int(time.time())), vals[1], vals[2], float(vals[5]), float(vals[6]), str(vals[37]), vals[3], int(vals[7]), int(vals[8]), vals[9], vals[10], vals[11],
        #         flightlevel_to_feet(vals[12]), vals[13], vals[21], vals[22], vals[28], vals[29].replace("\"", "").replace("'", ""), vals[30].replace("\"", "").replace("'", ""), int(vals[38]), "1")
        #         c.execute(inj)
        #         counter += 1
        #     except:
        #         #TO--DO Log the error here
        #         print("Error", vals[0:8], " . . .")
        #         continue
        # else:
        #     #TO--DO: log this because its not ATC or pilot!
        #     pass




















def flightlevel_to_feet(flightlevel):
    '''Function recieves something like 'FL360' and returns 36000'''

    if not(flightlevel):
        return 0

    flightlevel = str(flightlevel).lower()
    if "fl" in flightlevel or "f" in flightlevel:
        return int(flightlevel.replace("fl", "").replace("f", "")) * 100
    else:
        try:
            return int(flightlevel)
        except ValueError:
            return 0
