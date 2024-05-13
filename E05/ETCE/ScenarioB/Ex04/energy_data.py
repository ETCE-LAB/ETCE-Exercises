import os
import csv
import json
import pandas as pd
import numpy as np
i = 0
max_i = 720

data_folder = os.path.dirname(__file__)
energy_data = {}

with open(os.path.join(data_folder, "gb.sol.json")) as jsonfile:
   energy_data = json.loads(jsonfile.read())

with open(os.path.join(data_folder, 'timestamps.csv' ), newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        data_timestamp = row["yyyy-mm-dd hh:mm:ss.ms"]
        data_epoch = int(row["epoch"])
        index = int(row["index"])
        uuid = row["uuid"]
        energy_data[index] = dict(energy_data[str(index)])
        energy_data[index]["timestamp"] = data_epoch
        energy_data[index]["uuid"] = uuid
        for i in range(len(energy_data[index].keys()) - 2):
            energy_data[index][i] = energy_data[index][str(i)]
            del energy_data[index][str(i)]
        del energy_data[str( index )]
        home_ch = {'name': "Home Charger",
                   "location (lat,lon)":"52.534190, 13.444080",
                   "energy_providers":[{'total_ports': 1, 'data':
                                        {'Price per kWh (c€)': energy_data[index][1]["energy_providers"][-1]["data"]['Price per kWh (c€)'] * 1.0,
                                         'Minimum energy Purchase Amount (kWh)': 0,
                                         'Maximum energy Purchase Amount (kWh)': np.inf,
                                         'Free Charging Ports': 1},
                                        'name': 'Energy Provider 5',
                                        'Energy Source': 'Solar',
                                        'Carbon Footprint': '50gCO2eq/kWh'}]}


        for i in range(5):
            energy_data[index][str( i+1 )] = energy_data[index][i]

        for i in range(5):
            energy_data[index][i+1] = energy_data[index][str( i+1 )]
            del energy_data[index][str(i+1)]

        energy_data[index][0] = home_ch

def get_predictions():
    return energy_data

