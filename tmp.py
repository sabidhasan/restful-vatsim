import time, re
from functools import reduce

def parseTime(raw_time):
    ''' raw_time is either Unix time, or human readable time
    [now,today,yesterday]-[xhym, xh, ym, zs, 786876]'''
    #Try to parse the time
            #TO--DO: fix the times here
    time_codes = {"now": time.time(), "today": 0, "yesterday": 0}
    time_durations = {"d": 86400, "h": 3600, "m": 60, "s": 1}

    fixed_time = raw_time.split("-")

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
    adder = lambda acc, val: acc + (time_durations.get(val[-1], 0) * int(val[:-1]))
    try:
        #reduce(function, iterable, initial value for acc)
        end_duration = reduce(adder, time_objects, 0)
    except:
        #Unknown error
        print "Unknown error occured in parsing time"
        end_duration = 0

    return int(start_time - end_duration)

while True:
    x = raw_input("Enter a time ")
    print parseTime(x)
