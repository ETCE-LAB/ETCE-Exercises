import os
import csv
import json
i = 0
max_i = 720

data_folder = os.path.dirname(__file__)
weather_data = {}

with open(os.path.join(data_folder, "ga.sol.json")) as jsonfile:
   weather_data = json.loads(jsonfile.read())

with open(os.path.join(data_folder, 'timestamps.csv' ), newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        data_timestamp = row["yyyy-mm-dd hh:mm:ss.ms"]
        data_epoch = int(row["epoch"])
        index = int(row["index"])
        uuid = row["uuid"]
        weather_data[index] = dict(weather_data[str(index)])
        weather_data[index]["timestamp"] = data_epoch
        weather_data[index]["uuid"] = uuid
        weather_data[index]["clouds"] = min(max(0.0, weather_data[index]["clouds"]), 100.0)
        del weather_data[str( index )]

def get_predictions():
    return weather_data
