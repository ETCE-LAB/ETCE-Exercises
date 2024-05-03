import os
import csv
i = 0
max_i = 720

data_folder = os.path.dirname(__file__)

energy_data = []
energy_data_eval = []
timestamps = []

def get_file(source_num, ind, filetype):
    rm = {"json": "r",
          "bson": "rb",
          "xml": "r"}
    file_path = os.path.join(data_folder,
                             "multi_format/cs"+str(source_num)+"/"+str(ind)+"."+filetype)
    if os.path.isfile(file_path):
        with open(file_path, rm[filetype]) as wfile:
            return wfile.read()
    return energy_data[ind-1][source_num-1]

def get_file_eval(source_num, ind):
    file_path = os.path.join(data_folder,
                             "eval_json/cs"+str(source_num)+"/"+str(ind)+".json")
    if os.path.isfile(file_path):
        return file_path
    return energy_data_eval[ind-1][source_num-1]


with open(os.path.join(data_folder, 'timestamps.csv' ), newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        data_timestamp = row["yyyy-mm-dd hh:mm:ss.ms"]
        timestamps.append(data_timestamp)
        index = int(row["index"])
        energy_data.append((get_file(1, index, "json"),
                            get_file(2, index, "xml"),
                            get_file(3, index, "xml"),
                            get_file(4, index, "bson"),
                            get_file(5, index, "bson")))

def get_next():
    """
    Returns a Tuple (Charging Station 1, Charging Station 2, Charging
    Station 3, Charging Station 4, Charging Station 5) and a
    timestamp, i.e., Time of data calculation, in yyyy-mm-dd
    hh:mm:ss.ms CEST ((Charging Station 1, Charging Station 2,
    Charging Station 3, Charging Station 4, Charging Station 5), dt)

    """
    global i

    if not(i<max_i):
        raise Exception("No more energy data")
    ret = (energy_data[i][0],
           energy_data[i][1],
           energy_data[i][2],
           energy_data[i][3],
           energy_data[i][4])
    i = i + 1
    return ret, timestamps[i-1]


def get_next_eval():
    global i
    if not (i<max_i):
        raise Exception("errrrrr")
    data = []
    energy_data_eval.append((get_file_eval(1, i),
                             get_file_eval(2, i),
                             get_file_eval(3, i),
                             get_file_eval(4, i),
                             get_file_eval(5, i)))
    i = i + 1
    return energy_data_eval[-1]
