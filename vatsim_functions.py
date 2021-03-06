''' Constant functions for use by vatim classes module '''
import random, requests, re, datetime, time
from functools import reduce

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
        return None, None

    with open("vatsim_data.txt", 'wb') as f:
        f.write(data)
    return data, random_url

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

def vatsim_to_unix_time(vt):
    ''' Converts vatsim time (YYYYMMDDHHMMSS) into Unix time (seconds since epoch) '''
    times = map(lambda x: int(x), [vt[:4], vt[4:6], vt[6:8], vt[8:10], vt[10:12], vt[12:14]])

    return int((datetime.datetime(*times) - datetime.datetime(1970,1,1)).total_seconds())

################################################################################

def vatsim_to_num(data, num_function):
    ''' vatsim_to_num() takes raw data from the text file and tries to return
    it as a number, converted via num_function (either int or float) '''
    try:
        return num_function(data)
    except ValueError:
        return num_function(0)

################################################################################

def airport_from_callsign(callsign):
    ''' Takes "CYYZ_ATIS" or "CHI_W_GND" and returns "CYYZ", "CHI", etc. '''
    return callsign[0:4].replace("_", "")

################################################################################

def parseTime(raw_time):
    ''' parseTime() function takes a raw_time, which is either a Unix timestamp,
    or human readable time [now,today,yesterday]-[xhym, xh, ym, zs, 786876], and
    returns a unix timestamp from it'''
    #Trying to get UNIX time (secs since 1970/1/1) to make time_codes dictionary. For:
        # #1) this moment
        # #2) today's calendar date, when it started at midnight today
        # #3) yesterday's calendar date, at midnight yesteday
    #Define datetime objects for UTC_now, zero_time (1970) and exactly 24 h ago
    zero_time = datetime.datetime(1970, 1, 1)
    utc_time = datetime.datetime.utcnow()
    exact_yesterday = (utc_time - datetime.timedelta(1))

    #Unix epoch time is the difference in seconds from utctime to zero time
    now_in_unix = int((utc_time - zero_time).total_seconds())

    #Create a NEW datetime object with **only** yesterday's date, thereby ensuring
    #it starts at midnight - (no time information)
    yesterday_time = datetime.datetime(exact_yesterday.year, exact_yesterday.month, exact_yesterday.day)
    #Unix epoch time is the difference in seconds from yestarday-midnight to zero time
    yesterday_in_unix = int((yesterday_time - zero_time).total_seconds())

    #Create a NEW datetime object with **only** today's date, thereby ensuring
    #it starts at midnight - (no time information)
    today_time = datetime.datetime(utc_time.year, utc_time.month, utc_time.day)
    #Unix epoch time is the difference in seconds from today-midnight to zero time
    today_in_unix = int((today_time - zero_time).total_seconds())

    time_codes = {"now": now_in_unix, "today": today_in_unix, "yesterday": yesterday_in_unix}

    #Start parsing the time
    fixed_time = raw_time.replace(" ", "").split("-")

    #This is the "start" time (now, yesteday, today, etc.)
    start_time = time_codes.get(fixed_time[0], 0)

    if len(fixed_time) == 1: return int(start_time)

    #Regex for second time; time_objects is a tuple containing each group from regex
    end_duration = 0
    time_objects = re.search(r"^(\d*[d])?(\d*[h])?(\d*[m])?(\d*[s]?)?$", fixed_time[1])
    #was a valid search supplied?
    if not time_objects: return int(start_time)
    #Filter out the empties (regex returns None if that particular group was not found)
    time_objects = filter(None, list(time_objects.groups()))

    #Add up total duration (accumulator + value of that time duration) val = "15h"
    time_durations = {"d": 86400, "h": 3600, "m": 60, "s": 1}
    adder = lambda acc, val: acc + (time_durations.get(val[-1], 0) * int(val[:-1]))

    try:
        #reduce(function, iterable, initial value for acc)
        end_duration = reduce(adder, time_objects, 0)
    except:
        #Unknown error
        print "Unknown error occured in parsing time"
        end_duration = 0

    return int(start_time - end_duration)

################################################################################

def compare(local_data_value, user_requested_value, comparator_function):
    ''' Called as comparator function - if user requested value is substring
    of the local_data_value then there is a match '''
    #Comparison looks at local line and applies a comparator function
    #to compare it to user requested parameter. "in" keyword requires a
    #custom within function, because it's a keyword not a first order function\
    try:
        local_data_value = float(local_data_value)
        user_requested_value = float(user_requested_value)
    except ValueError:
        #item must be string so continue
        pass

    #Check if comparator worked - it is either True or returns
    return comparator_function(local_data_value, user_requested_value)

################################################################################

def minimum(local_data_value, user_requested_value):
    ''' minimum() is a slightly modified function for min() '''
    return min(local_data_value, user_requested_value) == local_data_value

################################################################################

def maximum(local_data_value, user_requested_value):
    ''' maximum() is a slightly modified function for min() '''
    return max(local_data_value, user_requested_value) == local_data_value

################################################################################

def within(local_data_value, user_requested_value):
     ''' within() is a make-do first order function for the in keyword '''
     return str(user_requested_value) in str(local_data_value)

################################################################################

def flightlevel_to_feet(flightlevel):
    '''The flightlevel_to_feet() function recieves something like 'FL360' or 1500
    and returns 36000 or 1500 '''

    #No altitude specified, so assume it is 0
    if not(flightlevel): return 0

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

################################################################################

def strip_fields(data_row, verbose_name, name_dictionary, user_requested_fields):
    ''' strip_fields() takes a row of data, verbose_name, dictionary of short-names
    to long-names (DB names) and a list of user requested fields (each a string)'''
    #No field supplied
    if not user_requested_fields:
        return data_row

    if verbose_name == "voice_servers":
        culled_row = {}
    else:
        culled_row = {"Vatsim ID": data_row["Vatsim ID"]}

    for internal_name in user_requested_fields:
        if not internal_name in name_dictionary:
            continue
        clean_name = name_dictionary.get(internal_name)
        culled_row[clean_name] = data_row[clean_name]

    if len(culled_row) == 0:
        return data_row
    return culled_row

################################################################################

def add_boiler_plate(data_array, source, time_updated, boiler_plate_text, end_index):
    ''' add_boiler_plate() takes a list of data, time_updated integer, boiler_plate_text
    and end_index (which is used for the limit parameter), adds boiler plate text
    (what is then returned in the first position of the array) '''
    #Define boiler plate
    num_rec = len(data_array) if end_index is None else end_index
    boiler_plate = {"Time Updated (UTC)": humanize_time(int(time_updated)),
        "Info": boiler_plate_text,
        "File Age (sec)": int(time.time() - time_updated),
        "Number of Records": num_rec,
        "Source": source}
    data_array.insert(0, boiler_plate)
    return data_array

################################################################################

def sort_on_field(data_array, user_sort_text, strip_fields_dict):
    ''' sort_on_field() sorts a full data array based on user_sort_text (?sort=heading,asc)
    and the long-name of the field (long name is what's included in the data_array)'''
    #Sort if needed, TO--DO: eror is if you are not seeing a field and sorting on it, it doesnt work
    if user_sort_text is not None:
        sort_field = user_sort_text.split(",")[0]

        sort_orders = {"asc": False, "dec": True}
        try:
            sort_order = user_sort_text.split(",")[1].lower()
        except IndexError:
            sort_order = ""
        sort_order = sort_orders.get(sort_order, False)

        try:
            data_array.sort(key=lambda x, i=strip_fields_dict[sort_field]: x[i], reverse=sort_order)
        except KeyError:
            pass
    return data_array

################################################################################

def controller_category_check(requested_category, current_callsign):
    ''' category_check() takes a requested category ("t" for tower or "c" for CTR)
    along with a row of data and returns True if the row is not of the right category
    '''
    #convert callsign to lowercase
    current_callsign = current_callsign.lower()

    if requested_category == "c" and not "ctr" in current_callsign:
        return True
    elif requested_category == "t" and ("ctr" in current_callsign or "sup" in current_callsign):
        return True
    return False

def pilot_category_check(requested_category, flight_type):
    return requested_category != flight_type
################################################################################

def humanize_time(epoch_time):
    ''' humanize_time() takes epoch UNIX time and returns human readable time '''
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(epoch_time))
