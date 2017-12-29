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
    #/api/v1/pilots/all                                              all VFR and IFR and other pilots

    #/api/v1/pilots/all/50000                                        identify by CID



    #/api/v1/pilots/all/?fields=groundspeed,heading                  only return specific fields

    #/api/v1/pilots/all/?callsign="AA"                                    callsign contains "AA"
    #/api/v1/pilots/all/?realname="Test"                                  identify by exact name

    #/api/v1/pilots/all/?min_latitude=50&maxlatitude=100                   identify by latitude
    #/api/v1/pilots/all/?min_longitude=50&maxlongitude=100                 identify by latitude
    #/api/v1/pilots/all/?min_altitude=0&maxaltitude=10000                  identify by altitude
    #/api/v1/pilots/all/?min_speed=0&maxspeed=0
    #/api/v1/pilots/all/?min_heading=0&maxheading=100

    #/api/v1/pilots/all/?dep_airport="CYVR"
    #/api/v1/pilots/all/?arr_airport="CYVR"
    #/api/v1/pilots/all/?in_route="YVR"




#return shoyld always have update time



#create cache object
#update function
    #if cache old, then update
    #return new data (either from cache or newly downloaded)

#download function
    #randomize source
    #download
