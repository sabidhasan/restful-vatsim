uses
    about to depart Aircraft
    busiest airports
    VA searching
    planes flying in a certain area
    planes violating speed rules (<250 kts <18000 ft)
    planes heading a certain direction
    who just signed in and got going quickly (logon time and min speed)
    who is currently saying they are streaming on twitch (remarks)
    fastest planes out there right now

#VOICE SERVER
    #/api/v1/voice_servers
    #/api/v1/voice_servers?name=London                                only servers with "london" as name
    #/api/v1/voice_servers?name=London&exactMatch=true                match exactly
    #/api/v1/voice_servers?limit=5                                    limit to 5
    #/api/v1/voice_servers?forceUpdate=True                           force a cache file update
    #/api/v1/voice_servers?fields=<field-names>                       limit fields to view
    #/api/v1/voice_servers?sort=<field-names>,asc                     what to sort on


#PILOTS
    #/api/v1/pilots                                                  all pilots

    #/api/v1/pilots/IFR                                              all pilots who are IFR
    #/api/v1/pilots/VFR
    #/api/v1/pilots/alltypes                                              all VFR and IFR and other pilots

    #/api/v1/pilots/alltypes/50000                                        identify by CID



    #/api/v1/pilots/alltypes/?fields=groundspeed,heading                  only return specific fields

    #/api/v1/pilots/alltypes/?callsign="AA"                                    callsign contains "AA"
    #/api/v1/pilots/alltypes/?realname="Test"                                  identify by exact name

    #/api/v1/pilots/alltypes/?min_latitude=50&max_latitude=100                   identify by latitude
    #/api/v1/pilots/alltypes/?min_longitude=50&max_longitude=100                 identify by latitude
    #/api/v1/pilots/alltypes/?min_altitude=0&max_altitude=FL100                  identify by altitude
    #/api/v1/pilots/alltypes/?min_speed=0&max_speed=0
    #/api/v1/pilots/alltypes/?min_heading=0&max_heading=100

    #/api/v1/pilots/alltypes/?dep_airport="CYVR"
    #/api/v1/pilots/alltypes/?arr_airport="CYVR"
    #/api/v1/pilots/alltypes/?in_route="YVR"                                    route contains yvr
    #/api/v1/pilots/alltypes/?aircraft="B777"                                   aircraft contains B777

    #/api/v1/pilots/alltypes/?min_logontime="now-5h4m"                             relative time (use h, m)
            # [now,today,yesterday]-[wd, xh, ym, zs, 786876]
    #/api/v1/pilots/alltypes/?max_logontime="38947389473"                           unix time

#CONTROLLER (client type is CONTROLLER)
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
