'''
Module contains helper functions for main.py for restful_vatsim
'''

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


def jsonify_data(data):
    ''' jsonify_data() makes recieved raw VATSIM.txt data usable by trimming the
    fat, parsing for errors, and making data easily searchable '''
    pass

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
