const data = [
  {
    title: "VOICE SERVERS",
    stuff: [
      ["#/api/v1/voice_servers", "all voice servers currently online"],
      ["#/api/v1/voice_servers?name=London", "servers with 'london' within name"],
      ["#/api/v1/voice_servers?name=London&amp;exactMatch=true", "match name exactly"],
      ["#/api/v1/voice_servers?limit=5", "limit results to 5"],
      ["#/api/v1/voice_servers?forceUpdate=True", "force a cache file update - otherwise requests are cached for 2 min"],
      ["#/api/v1/voice_servers?fields=< field-names >", "(comma separated) limit fields in returned data"],
      ["#/api/v1/voice_servers?sort=< field-name ><,asc>", "sort data by field - asc / dec is optional (asc is default)"]
    ],
    "trailer": ["< field-names >", "location, address, name, host_name, clients_allowed"]
  },
  {
    "title": "CONTROLLERS",
    "stuff": [
      ["#/api/v1/controllers/", "all controllers"],
      ["#api/v1/controllers/centers", "all center controllers (have 'CTR' in callsign)"],
      ["#api/v1/controllers/towers", "all tower controllers (don't have 'CTR' or 'SUP' in callsign)"],
      ["#api/v1/controllers/alltypes", "all controllers (same as /api/v1/controllers)"],
      ["#api/v1/controllers/alltypes/50000", "limit by specific Vatsim ID"],
      ["#/api/v1/controllers/alltypes/?callsign='KORD_W_APP'", "limit by text within callsign"],
      ["#/api/v1/controllers/alltypes/?airport='EDDM'", "limit by text within airport ICAO/IATA code"],
      ["#/api/v1/controllers/alltypes/?real_name='Edward'", "identify records where real name contains text"],
      ["#/api/v1/controllers/alltypes/?min_latitude=50&amp;maxlatitude=100", "limit by latitude"],
      ["#/api/v1/controllers/alltypes/?min_longitude=50&amp;maxlongitude=100", "limit by longitude"],
      ["#/api/v1/controllers/alltypes/?frequency=124.95", "identify by frequency"],
      ["#/api/v1/controllers/alltypes/?atis='snow'", "identify by ATIS content"],
      ["#/api/v1/controllers/alltypes/?logontime<='now-5h4m'", "limit by logon time - [now,today,yesterday]-[#d, #h, #m, #s]"],
      ["#/api/v1/controllers/alltypes/?logontime=38947389473", "limit by logon time - uses absolute unix time"],
      ["#/api/v1/controllers?limit=5", "limit results to 5"],
      ["#/api/v1/controllers?forceUpdate=True", "force a cache file update - otherwise requests are cached for 2 min"],
      ["#/api/v1/controllers?fields=< field-names >", "(comma separated) limit fields in returned data"],
      ["#/api/v1/controllers?sort=< field-name ><,asc>", "sort data by field - asc / dec is optional (asc is default)"]
    ],
    "trailer": ["< field-names >", `callsign, vatsim_id, real_name, latitude, longitude, login_time,
                altitude, ground_speed, heading, route, remarks, planned_aircraft, airport_destination,
                airport_origin, planned_altitude, flight_type, time`]
  },
  {
    title: "PILOTS",
    stuff: [
      ["#/api/v1/pilots", "all pilots"],
      ["#/api/v1/pilots/IFR", "all IFR pilots"],
      ["#/api/v1/pilots/VFR", "all VFR pilots"],
      ["#/api/v1/pilots/alltypes", "all pilots (same as /api/v1/pilots)"],
      ["#/api/v1/pilots/alltypes/50000", "identify by Vatsim ID"],
      ["#/api/v1/pilots/alltypes/?callsign=AA", "callsign contains 'AA'"],
      ["#/api/v1/pilots/alltypes/?realname='John'", "name contains John"],
      ["#/api/v1/pilots/alltypes/?min_latitude=50&amp;max_latitude=100", "limit by latitude range"],
      ["#/api/v1/pilots/alltypes/?min_longitude=50&amp;max_longitude=100", "limit by longitude range"],
      ["#/api/v1/pilots/alltypes/?min_altitude=10000&amp;max_altitude=FL190", "limit by altitude range (altitude can be <FL350> or <35000>)"],
      ["#/api/v1/pilots/alltypes/?min_speed=0&amp;max_speed=200", "limit by speed range"],
      ["#/api/v1/pilots/alltypes/?min_heading=0&amp;max_heading=100", "limit by heading range"],
      ["#/api/v1/pilots/alltypes/?dep_airport='CYVR'", "airport contains 'CYVR'"],
      ["#/api/v1/pilots/alltypes/?in_route='YVR'", "filed route contains 'YVR'"],
      ["#/api/v1/pilots/alltypes/?aircraft='B777'", "aircraft field contains 'B777'"],
      ["#/api/v1/pilots/alltypes/?min_logontime='now-5h4m'", "limit by logon time [now,today,yesterday]-[#d, #h, #m, #s]"],
      ["#/api/v1/pilots/alltypes/?max_logontime='38947389473'", "limit by logon time - uses absolute unix time"],
      ["#/api/v1/pilots?limit=5", "limit results to 5"],
      ["#/api/v1/pilots?forceUpdate=True", "force a cache file update - otherwise requests are cached for 2 min"],
      ["#/api/v1/pilots?fields=<field-names>", "(comma separated) limit fields in returned data"],
      ["#/api/v1/pilots?sort=<field-name><,asc>", "sort data by field - asc / dec is optional (asc is default)"]
    ],
    "trailer": ["#Possible < field-names >", `callsign, vatsim_id, real_name, latitude, longitude, login_time
    altitude, ground_speed, heading, route, remarks, planned_aircraft, airport_destination, airport_origin,
    planned_altitude, flight_type, time`]
  }
]

function populateHelp() {
  let helpTable = document.querySelector(".help-table")
  let text = ""
  // Loop through data and add to table
  for (let thing in data) {

    text += `<tr><td class="table-text">${data[thing].title}</td></tr>`
    for (let item in data[thing].stuff) {
      console.log(item)
      if (data[thing].stuff[item][0].split("?").length === 2) {
        data[thing].stuff[item][0] = data[thing].stuff[item][0].split("?")[0] + `?<span class="hl">${data[thing].stuff[item][0].split("?")[1]}</span>`
      }
      text += `<tr> <td>${data[thing].stuff[item][0]}</td> <td>${data[thing].stuff[item][1]}</td> </tr>`
    }
    text += `<tr><td>${data[thing].trailer[0]}<br/><span class="indented">${data[thing].trailer[1]}</span></td></tr>`

  }


  helpTable.innerHTML = text
}
//""
//
