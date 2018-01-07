uses
    about to depart Aircraft
    busiest airports
    VA searching
    planes flying in a certain area
    planes violating speed rules (<250 kts <18000 ft)
    planes heading a certain direction
    who just signed in and got going quickly

#VOICE SERVER
    #/api/v1/voice_servers
    #/api/v1/voice_servers?name=London                                only servers with "london" as name
    #/api/v1/voice_servers?name=London&exactMatch=true                match exactly
    #/api/v1/voice_servers?limit=5                                    limit to 5
    #/api/v1/voice_servers?forceUpdate=True                           force a cache file update






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
