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
    #/api/v1/pilots                                                   all pilots

    #/api/v1/pilots/IFR                                               all pilots who are IFR
    #/api/v1/pilots/VFR                                               all pilots who are VFR
    #/api/v1/pilots/alltypes                                          all VFR and IFR and other pilots

    #/api/v1/pilots/alltypes/50000                                    identify by CID

    #/api/v1/pilots/alltypes/?callsign="AA"                           callsign contains "AA"
    #/api/v1/pilots/alltypes/?realname="Test"                         name contains Test

    #/api/v1/pilots/alltypes/?min_latitude=50&max_latitude=100        identify by latitude
    #/api/v1/pilots/alltypes/?min_longitude=50&max_longitude=100      identify by latitude
    #/api/v1/pilots/alltypes/?min_altitude=0&max_altitude=FL100       identify by altitude
    #/api/v1/pilots/alltypes/?min_altitude=0&max_altitude=35000       identify by altitude
    #/api/v1/pilots/alltypes/?min_speed=0&max_speed=0                 identify by speed
    #/api/v1/pilots/alltypes/?min_heading=0&max_heading=100           identify by heading

    #/api/v1/pilots/alltypes/?dep_airport="CYVR"                      limit by airport
    #/api/v1/pilots/alltypes/?arr_airport="CYVR"                      limit by airport
    #/api/v1/pilots/alltypes/?in_route="YVR"                          route contains yvr
    #/api/v1/pilots/alltypes/?aircraft="B777"                         aircraft contains B777

    #/api/v1/pilots/alltypes/?min_logontime="now-5h4m"                relative time [now, today, yesterday]-(d, h, m, s)
            # [now,today,yesterday]-[wd, xh, ym, zs, 786876]
    #/api/v1/pilots/alltypes/?max_logontime="38947389473"             absolute unix time

    #/api/v1/voice_servers?limit=5                                    limit results to 5
    #/api/v1/voice_servers?forceUpdate=True                           force a cache file update
    #/api/v1/voice_servers?fields=<field-names>                       limit fields to view
    #/api/v1/voice_servers?sort=<field-names>,asc                     what to sort by and how to sort (optional)


#CONTROLLERS
    #/api/v1/controllers/                                             all atc online

    #api/v1/controllers/centers                                       type center (has CTR in name)
    #api/v1/controllers/towers                                        type tower (doesnt have CTR or SUP in name)
    #api/v1/controllers/alltypes                                      type all of the above (centers, towers and supervisors)

    #api/v1/controllers/alltypes/50000                                limit by specific CID

    #/api/v1/controllers/alltypes/?callsign="EDDM"                    identify where callsign contains ...
    #/api/v1/controllers/alltypes/?real_name="Edward"                 identify records where name contains ...

    #/api/v1/controllers/alltypes/?min_latitude=50&maxlatitude=100    by latitude
    #/api/v1/controllers/alltypes/?min_longitude=50&maxlongitude=100  by longitude

    #/api/v1/controllers/alltypes/?frequency=124.95                   identify by freq.

    #/api/v1/controllers/alltypes/?atis="military"                    ATIS text content

    #/api/v1/controllers/alltypes/?logontime<="now-5h4m"              relative time (use h, m)
    #/api/v1/controllers/alltypes/?logontime>"38947389473"            unix time

    #/api/v1/voice_servers?limit=5                                    limit results to 5
    #/api/v1/voice_servers?forceUpdate=True                           force a cache file update
    #/api/v1/voice_servers?fields=<field-names>                       limit fields to view
    #/api/v1/voice_servers?sort=<field-names>,asc                     what to sort by and how to sort (optional)
