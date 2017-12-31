#VOICE SERVER
    #/api/v1/voiceServers
    #/api/v1/voiceServers?name=London                                only servers with "london" as name
    #/api/v1/voiceServers?name=London&exactMatch=true                match exactly
    #/api/v1/voiceServers?limit=5                                    limit to 5
    #/api/v1/voiceServers?hostname='vatsim.net'                      only servers with "vatsim.net" in host

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
import requests, random, time

#create flask app
app = Flask(__name__)
api = Api(app)

#Memoization for latest data
latest_file = {'time_updated': 0, 'file': None}

#Generic function definitions

def get_latest_data():
    '''get_latest_data() checks for data freshness in the local cache and if
    data is too old, then it fetches new data. It then returns freshest data'''
    #Check cache freshness; call download if needed
    if (latest_file["time_updated"] + 120) < int(time.time()):
        #Needs updating
        new_file = download()
        if new_file is not None:
            latest_file["time_updated"] = int(time.time())
            latest_file["file"] = new_file
        else:
            print "Downloaded file not valid"
    #Return newest data
    return latest_file["file"]


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
