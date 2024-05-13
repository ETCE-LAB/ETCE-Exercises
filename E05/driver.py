import json
import numbers
from decimal import Decimal


class ETCEFloat(float):
    def __init__(self, value, eps=0.01):
        self.eps = eps
        super(ETCEFloat, self).__init__()

    def __eq__(self, other):
        return (abs(Decimal(str(self)) - Decimal(str(other))) <= self.eps)

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
        return [1.0, 2.0, {"a": 3, "b": [4.001]}] == ETCEList([1.01, 1.99, {"a": 3.01, "b": [4]}]) and ETCEList(
            [1.01, 1.99, {"a": 3.01, "b": [4]}]) == [1.0, 2.0, {"a": 3, "b": [4.001]}]


class ETCEDict(dict):
    def __init__(self, value, eps=0.01):
        self.eps = eps
        super(ETCEDict, self).__init__(value)

    def __eq__(self, other):
        return {k: ETCEFloat.changeToETCEFloat(v, eps=self.eps) for k, v in self.items()} == (other)

    def __getitem__(self, key):
        return ETCEFloat.changeToETCEFloat(super(ETCEDict, self).__getitem__(key), self.eps)


class ETCEList(list):
    def __init__(self, value, eps=0.01):
        self.eps = eps
        super(ETCEList, self).__init__(value)

    def __eq__(self, other):
        return [ETCEFloat.changeToETCEFloat(v, eps=self.eps) for v in self] == (other)

    def __getitem__(self, key):
        return ETCEFloat.changeToETCEFloat(super(ETCEList, self).__getitem__(key), self.eps)


def check_solution_A(
        solution, solar, wind
):
    example_solution = """(({<integer timestamp>:
     {"power_output":<float (kW)>,
      "energy_accumulated":<float kWh>},
   ...,
  },
   <float average power output in %>),
 ({<integer timestamp>:
     {"power_output":<float (kW)>,
      "energy_accumulated":<float kWh>},
   ...,
  },
   <float average power output in %>))"""

    sol_a = solution()
    sol_a_json = None
    with open("ga.sol.json") as jsonfile:
        sol_a_json = ETCEList(json.loads(jsonfile.read()))
    structure_pass = ((len(sol_a) == 2) and
                      (len(sol_a[0]) == 2) and
                      (len(sol_a[1]) == 2))

    if not structure_pass:
        print("Incorrect solution structure. There might be exceptions \
while checking your solution. Please make sure the `solution()` \
returns a datastructure of the form: ")
        print(example_solution)

    solar_tests = [({'uuid': '00000000',
                     'timestamp': 1618047000,
                     'temp': 5.33,
                     'clouds': 10,
                     'wind_speed': 10,
                     'wind_deg': 31.0,
                     'wind_gust': 4.1,
                     'rain': 1.54}, 45.5),
                   ({'uuid': '00000000',
                     'timestamp': 1618017000,
                     'temp': 5.33,
                     'clouds': 10,
                     'wind_speed': 10,
                     'wind_deg': 31.0,
                     'wind_gust': 4.1,
                     'rain': 1.54}, 0.0)]

    wind_tests = [({'uuid': '00000000',
                    'timestamp': 1618047000,
                    'temp': 5.33,
                    'clouds': 10,
                    'wind_speed': 10,
                    'wind_deg': 31.0,
                    'wind_gust': 4.1,
                    'rain': 1.54}, 43.75),
                  ({'uuid': '00000000',
                    'timestamp': 1618017000,
                    'temp': 5.33,
                    'clouds': 10,
                    'wind_speed': 2.7,
                    'wind_deg': 31.0,
                    'wind_gust': 4.1,
                    'rain': 1.54}, 0.0)]

    solar_unit_pass = (solar(solar_tests[0][0]) == ETCEFloat(solar_tests[0][1])) and (
                solar(solar_tests[1][0]) == ETCEFloat(solar_tests[1][1]))

    if not solar_unit_pass:
        print("The `solar()` function is not predicting the power output \
of the solar farm correctly. Please check your computations.\
Also remember that you have to convert the timestamp to CEST")

    wind_unit_pass = (wind(wind_tests[0][0]) == ETCEFloat(wind_tests[0][1])) and (
                wind(wind_tests[1][0]) == ETCEFloat(wind_tests[1][1]))

    if not wind_unit_pass:
        print("The `wind()` function is not predicting the power output \
of the wind farm correctly. Please check your computations, and the \
definitions of `cut-in speed` and `rated speed` of a wind turbine.")

    solar_avg_pass = (sol_a[0][1] == ETCEFloat(sol_a_json[0][1]))
    wind_avg_pass = (sol_a[1][1] == ETCEFloat(sol_a_json[1][1]))

    if not solar_avg_pass:
        print(f"The average power output (%) of the solar farm must be = \
{sol_a_json[0][1]} (Got {sol_a[0][1]}). Check your power output calculations.")
    if not wind_avg_pass:
        print(f"The average power output (%) of the wind farm must be = \
{sol_a_json[1][1]} (Got {sol_a[1][1]}). Check your power output calculations.")

    avg_pass = ((sol_a[0][1] == ETCEFloat(sol_a_json[0][1])) and
                (sol_a[1][1] == ETCEFloat(sol_a_json[1][1])))

    sol_a_json_solar = {}
    for k in sol_a_json[0][0].keys():
        sol_a_json_solar[int(k)] = sol_a_json[0][0][k]
    sol_a_json_wind = {}
    for k in sol_a_json[1][0].keys():
        sol_a_json_wind[int(k)] = sol_a_json[1][0][k]

    solar_pass = sol_a[0][0] == ETCEDict(sol_a_json_solar)
    wind_pass = sol_a[1][0] == ETCEDict(sol_a_json_wind)

    if not solar_pass:
        print("Some or all of your power output predictions for the solar farm \
are incorrect.")
    if not wind_pass:
        print("Some or all of your power output predictions for the wind farm \
are incorrect.")

    return (structure_pass, avg_pass, solar_unit_pass, wind_unit_pass, solar_pass, wind_pass)


def evaluation(
        solution, solar, wind
):
    """
    This method computes the evaluation based on a weighting factor
    """
    weighting_a = (.05, .05, .40, .40, .05, .05)

    evaluation_A = 0
    try:
        for (success, weight) in zip(
            check_solution_A(
                solution,
                solar,
                wind,
            ),
            weighting_a,
        ):
            if success:
                evaluation_A += weight
    except Exception as E:
        print("solution() failed to run:")
        raise (E)
    return (evaluation_A * 100,)


def evaluate(
        solution, solar, wind
):
    e = evaluation(
        solution,
        solar,
        wind,
    )

    print(f"Grade = {e[0]}%")

    if e[0] == 100:
        print("Perfect Score")
