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





#do imports

#create flask app

#create cache object

#  *update* function
    #if cache old, then call *download*
    #return new data (either from cache or newly downloaded)

#  *download* function
    #randomize source
    #download

# *flightlevel_to_feet* from cronupdater    - for parsing flight level


# *routes*
