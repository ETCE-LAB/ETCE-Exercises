import os
import csv
import pandas as pd
i = 0
max_i = 720

data_folder = os.path.dirname(__file__)

owm_notes = "`dt` : Time of data calculation, in yyyy-mm-dd hh:mm:ss.ms CEST\n"
owm_notes+= "`temp` : Temperature, °C\n"
owm_notes+= "`feels_like` : Temperature, °C. This temperature parameter accounts for the human perception of weather\n"
owm_notes+= "`pressure` : Atmospheric pressure (on the sea level, if there is no sea_level or grnd_level data), hPa\n"
owm_notes+= "`humidity` : Humidity, %\n"
owm_notes+= "`dew_point` : Dew Point, in °C\n"
owm_notes+= "`wind_speed` : Wind speed. Unit: meter/sec.\n"
owm_notes+= "`wind_deg` : Wind direction, degrees (meteorological)\n"
owm_notes+= "`clouds` : Cloudiness, %\n"
owm_notes+= "`rain_over_last_1h` : Rain Volume, over last 1 hour\n"

tmp36_notes = "Output Voltage readings from a TMP36 temperature sensor located atop Charging Station"

descriptions = [{"name":"Weather Source 1",
                 "lat":52.561141,  
                 "lon":13.295504,
                 "type":"String representing `json` data",
                 "notes":owm_notes},
                {"name":"Weather Source 2",
                 "lat":52.531240,  
                 "lon":13.352278,
                 "type":"String representing `json` data",
                 "notes":owm_notes},
                {"name":"Weather Source 3",
                 "lat":52.555666,  
                 "lon":13.463309,
                 "type":"Python `bytes` object representing `bson` data",
                 "notes":owm_notes},
                {"name":"Weather Source 4",
                 "lat":52.488049, 
                 "lon":13.382281,
                 "type":"String representing `xml` data",
                 "notes":owm_notes},
                {"name":"TMP36 Sensor",
                 "lat":52.511300,
                 "lon":13.400800,
                 "type":"String representing `xml` data",
                 "notes":tmp36_notes}]

weather_data = []
weather_data_eval = []
timestamps = []
def get_file(source_num, ind, filetype):
    rm = {"json": "r",
          "bson": "rb",
          "xml": "r"}
    file_path = os.path.join(data_folder,
                             "multi_format/ws"+str(source_num)+"/"+str(ind)+"."+filetype)
    if os.path.isfile(file_path):
        with open(file_path, rm[filetype]) as wfile:
            return wfile.read()
    return weather_data[ind-1][source_num-1]

def get_file_eval(source_num, ind):
    file_path = os.path.join(data_folder,
                             "eval_csv/ws"+str(source_num)+"/"+str(ind)+".json")
    if os.path.isfile(file_path):
        return file_path
    return weather_data_eval[ind-1][source_num-1]


with open(os.path.join(data_folder, 'timestamps.csv' ), newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        data_timestamp = row["yyyy-mm-dd hh:mm:ss.ms"]
        timestamps.append(data_timestamp)
        index = int(row["index"])
        weather_data.append((get_file(1, index, "json"),
                             get_file(2, index, "json"),
                             get_file(3, index, "bson"),
                             get_file(4, index, "xml"),
                             get_file(5, index, "xml")))

def get_next():
    """Returns a Tuple (Source 1, Source 2, Source 3, Source 4,
    Source 5) and a timestamp, i.e., Time of data calculation, in
    yyyy-mm-dd hh:mm:ss.ms CEST ((Source1, Source2, Source 3, Source
    4, Source 5), dt)

    """
    global i

    if not(i<max_i):
        raise Exception("No more weather data")
    ret = ({"description": descriptions[0], "data": weather_data[i][0]},
           {"description": descriptions[1], "data": weather_data[i][1]},
           {"description": descriptions[2], "data": weather_data[i][2]},
           {"description": descriptions[3], "data": weather_data[i][3]},
           {"description": descriptions[4], "data": weather_data[i][4]})
    i = i + 1
    return ret, timestamps[i-1]

def get_next_eval():
    global i
    if not (i<max_i):
        raise Exception("Error in Eval")
    data = []
    weather_data_eval.append((get_file_eval(1, i),
                              get_file_eval(2, i),
                              get_file_eval(3, i),
                              get_file_eval(4, i),
                              get_file_eval(5, i)))
    i = i + 1
    return weather_data_eval[-1]
