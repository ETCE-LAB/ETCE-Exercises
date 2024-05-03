import os
import pandas as pd
from uuid import UUID
import json
import numbers
from decimal import Decimal
import nbimporter


class ETCEFloat(float):
    def __init__(self, value, eps=0.01):
        self.eps = eps
        super(ETCEFloat, self).__init__()

    def __eq__(self, other):
        return abs(Decimal(str(self)) - Decimal(str(other))) <= self.eps

    def changeToETCEFloat(value, eps=0.01):
        if isinstance(value, numbers.Number):
            return ETCEFloat(value, eps=eps)
        elif isinstance(value, dict):
            return ETCEDict(value, eps=eps)
        elif isinstance(value, list):
            return ETCEList(value, eps=eps)
        else:
            return value

    def __test__(self):
        return [1.0, 2.0, {"a": 3, "b": [4.001]}] == ETCEList(
            [1.01, 1.99, {"a": 3.01, "b": [4]}]
        ) and ETCEList([1.01, 1.99, {"a": 3.01, "b": [4]}]) == [
            1.0,
            2.0,
            {"a": 3, "b": [4.001]},
        ]


class ETCEDict(dict):
    def __init__(self, value, eps=0.01):
        self.eps = eps
        super(ETCEDict, self).__init__(value)

    def __eq__(self, other):
        return {
            k: ETCEFloat.changeToETCEFloat(v, eps=self.eps) for k, v in self.items()
        } == (other)

    def __getitem__(self, key):
        return ETCEFloat.changeToETCEFloat(
            super(ETCEDict, self).__getitem__(key), self.eps
        )


class ETCEList(list):
    def __init__(self, value, eps=0.01):
        self.eps = eps
        super(ETCEList, self).__init__(value)

    def __eq__(self, other):
        return [ETCEFloat.changeToETCEFloat(v, eps=self.eps) for v in self] == (other)

    def __getitem__(self, key):
        return ETCEFloat.changeToETCEFloat(
            super(ETCEList, self).__getitem__(key), self.eps
        )


def isUUID(some_string):
    Pass = True
    try:
        UUID(some_string)
    except Exception:
        Pass = False
        print(f"{some_string} is not a valid UUID")
    return Pass


def check_json_parser() -> bool:
    pass_json = False
    try:
        with open(
            os.path.join("ETCE/GroupA/Ex03/multi_format/ws1/11.json"), "r"
        ) as jsonfile:
            json_data = jsonfile.read()
            pass_json = parse_json(json_data) == ETCEDict(
                {
                    "temp": 5.33,
                    "clouds": 100.0,
                    "wind_speed": 2.48,
                    "wind_deg": 31.0,
                    "wind_gust": 4.1,
                    "rain": 1.54,
                }
            )
    except Exception as E:
        print("Could not test json parser.")
        raise E
    return pass_json


def check_bson_parser() -> bool:
    pass_bson = False
    try:
        with open("ETCE/GroupA/Ex03/multi_format/ws3/100.bson", "rb") as bsonfile:
            bson_data = bsonfile.read()
            pass_bson = parse_bson(bson_data) == ETCEDict(
                {
                    "temp": 9.03,
                    "clouds": 75.95,
                    "wind_speed": 3.65,
                    "wind_deg": 106.99,
                    "wind_gust": 4.17,
                    "rain": 1.03,
                }
            )

    except Exception as E:
        print("Could not test bson parser.")
        raise E
    return pass_bson


def check_xml_parser() -> bool:
    pass_xml = False
    try:
        with open("ETCE/GroupA/Ex03/multi_format/ws4/7.xml", "r") as xmlfile:
            xml_data = xmlfile.read()
            pass_xml = parse_xml(xml_data) == ETCEDict(
                {
                    "temp": 5.34,
                    "clouds": 100.05,
                    "wind_speed": 2.55,
                    "wind_deg": 31.16,
                    "wind_gust": 4.18,
                    "rain": 1.55,
                }
            )
    except Exception as E:
        print("Could not test xml parser.")
        raise E
    return pass_xml


def check_volts_parser() -> bool:
    pass_volts = False
    try:
        with open("ETCE/GroupA/Ex03/multi_format/ws5/4.xml", "r") as voltsfile:
            volts_data = voltsfile.read()
            pass_volts = parse_volts(volts_data) == ETCEDict({"temp": 5.33})
    except Exception as E:
        print("Could not test volts parser.")
        raise E
    return pass_volts


def check_solution_A():
    sol_a = solution()
    sol_a_json = None
    with open("ga.sol.json") as jsonfile:
        sol_a_json = ETCEDict(json.loads(jsonfile.read()))
        # This file contains the expected solution_dict expected

    try:
        uuids = pd.DataFrame([sol_a[k]["uuid"] for k in sol_a.keys()])
    except Exception as E:
        print("Could not read UUIDs")
        raise E
    try:
        pass_uuid = uuids[0].apply(isUUID).all()
    except KeyError:
        print("Your solution() did not return a dictionary with any keys")
        return (0,)
    except Exception as E:
        print(
            "Could not validate some UUIDs. Some of your UUIDs are \
not valid"
        )
        raise E

    pass_uniq_uuids = len(uuids[0]) == len(list(dict.fromkeys(list(uuids[0]))))
    try:
        ts = [sol_a[k]["timestamp"] for k in sol_a.keys()]
    except Exception as E:
        print("Could not read Timestamps")
        raise E
    try:
        pass_timestamps = (
            min(ts) >= 1618012800
            and max(ts) <= 1618444200
            and len(ts) == len(list(dict.fromkeys(ts)))
        )
    except Exception as E:
        print("Could not validate Timestamps")
        raise E

    if not pass_timestamps:
        print(
            "Please check parse_timestamp(). Remember to return a \
timestamp in the correct timezone"
        )

    pass_json = check_json_parser()
    pass_bson = check_bson_parser()
    pass_xml = check_xml_parser()
    pass_volts = check_volts_parser()

    if not pass_json:
        print("parse_json() is not correct")
    if not pass_bson:
        print("parse_bson() is not correct")
    if not pass_xml:
        print("parse_xml() is not correct")
    if not pass_volts:
        print("parse_volts() is not correct")

    try:
        temp = [sol_a[k]["temp"] for k in sol_a.keys()]
    except Exception as E:
        print("Could not read temp")
        raise E

    temp_s = [sol_a_json[k]["temp"] for k in sol_a_json.keys()]
    pass_temp = None
    try:
        pass_temp = temp == temp_s
    except Exception as E:
        print("Could not grade temp")
        raise E

    if not pass_temp:
        print("The averaged temperature values are not accurate")

    try:
        clouds = [sol_a[k]["clouds"] for k in sol_a.keys()]
    except Exception as E:
        print("Could not read clouds")
        raise E

    clouds_s = [sol_a_json[k]["clouds"] for k in sol_a_json.keys()]
    pass_clouds = None
    try:
        pass_clouds = clouds == clouds_s
    except Exception as E:
        print("Could not grade clouds")
        raise E

    if not pass_clouds:
        print("The averaged clouds values are not accurate")

    try:
        wind_speed = [sol_a[k]["wind_speed"] for k in sol_a.keys()]
    except Exception as E:
        print("Could not read wind_speed")
        raise E

    wind_speed_s = [sol_a_json[k]["wind_speed"] for k in sol_a_json.keys()]
    pass_wind_speed = False
    try:
        pass_wind_speed = wind_speed == wind_speed_s
    except Exception as E:
        print("Could not grade wind_speed")
        raise E

    if not pass_wind_speed:
        print("The averaged wind_speed values are not accurate")

    try:
        wind_deg = [sol_a[k]["wind_deg"] for k in sol_a.keys()]
    except Exception as E:
        print("Could not read wind_deg")
        raise E

    wind_deg_s = [sol_a_json[k]["wind_deg"] for k in sol_a_json.keys()]
    pass_wind_deg = False
    try:
        pass_wind_deg = wind_deg == wind_deg_s
    except Exception as E:
        print("Could not grade wind_deg")
        raise E

    if not pass_wind_deg:
        print("The averaged wind_deg values are not accurate")

    try:
        wind_gust = [sol_a[k]["wind_gust"] for k in sol_a.keys()]
    except Exception as E:
        print("Could not read wind_gust")
        raise E

    wind_gust_s = [sol_a_json[k]["wind_gust"] for k in sol_a_json.keys()]

    pass_wind_gust = False
    try:
        pass_wind_gust = wind_gust == wind_gust_s
    except Exception as E:
        print("Could not grade wind_gust")
        raise E

    if not pass_wind_gust:
        print("The averaged wind_gust values are not accurate")

    try:
        rain = [sol_a[k]["rain"] for k in sol_a.keys()]
    except Exception as E:
        print("Could not read rain")
        raise E

    rain_s = [sol_a_json[k]["rain"] for k in sol_a_json.keys()]

    pass_rain = False
    try:
        pass_rain = rain == rain_s
    except Exception as E:
        print("Could not grade rain")
        raise E

    if not pass_rain:
        print("The averaged rain values are not accurate")

    return (
        pass_uuid,
        pass_uniq_uuids,
        pass_timestamps,
        pass_json,
        pass_bson,
        pass_xml,
        pass_volts,
        pass_temp
        and pass_clouds
        and pass_wind_speed
        and pass_wind_deg
        and pass_wind_gust
        and pass_rain,
    )


def check_ts_B(b_sol, b_sol_dict):
    Pass = True
    for i in b_sol.keys():
        for j in range(5):
            Pass = b_sol[i][j] == b_sol_dict[str(i)][str(j)]
            if not Pass:
                return False
    return True


aa = None


def evaluation():
    """
    This method computes the evaluation based on a weighting factor
    """
    global aa
    weighting_a = (0.05, 0.05, 0.05, 0.2, 0.2, 0.2, 0.2, 0.05)

    evaluation_A = 0
    try:
        for success, weight in zip(check_solution_A(), weighting_a):
            if success:
                evaluation_A += weight
    except Exception as E:
        print("E04 task failed to run:")
        raise E

    return (evaluation_A * 100,)


e = evaluation()

print(f"Grade = {e[0]}%")

if e[0] == 100:
    print("Perfect Score")
