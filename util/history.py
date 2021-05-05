import datetime
import json
from itertools import islice


# Clear history
def clear_history():
    try:
        with open("history.txt", "w") as f:
            zeros = {'Month': 0, 'Year': 0,
                     'Cold water': 0, 'Cold water payment': 0,
                     'Hot water': 0, 'Hot water payment': 0,
                     'Electricity': 0, 'Electricity payment': 0,
                     'Total Money': 0}
            print(zeros, file=f)
    except Exception as e:
        print(e)


# Save data to the history file
def append_history(cold_water, cold_water_payment,
                   hot_water, hot_water_payment,
                   electricity, electricity_payment,
                   total_payment):

    # Corrent date
    current_date = datetime.datetime.now()
    month = int(current_date.strftime("%m"))
    yaear = int(current_date.strftime("%y"))

    # Create JSON
    data = "{"
    data += f"\'Month\':{month},"
    data += f" \'Year\':{yaear},"
    data += f" \'Cold water\':{round(cold_water, 2)},"
    data += f" \'Cold water payment\':{round(cold_water_payment, 2)},"
    data += f" \'Hot water\':{round(hot_water, 2)},"
    data += f" \'Hot water payment\':{round(hot_water_payment, 2)},"
    data += f" \'Electricity\':{round(electricity, 2)},"
    data += f" \'Electricity payment\':{round(electricity_payment, 2)},"
    data += f" \'Total Payment\':{round(total_payment, 2)}"
    data += "}"

    # Add JSON data to txt file
    with open("history.txt", "a") as f:
        print(data, file=f)


# Read history from file
def get_history():
    history = []
    try:
        with open('history.txt') as f:
            for line in islice(f, 0, None):
                json_acceptable_string = line.replace("'", "\"")
                d = json.loads(json_acceptable_string)
                history.insert(0, d)
    except:
        # Create history.txt
        clear_history()
        # Return history using recursion
        history = get_history()
    return history


# Return latest counters from history, if history is empty append zeros to file.
def get_latest_readings():
    history = get_history()
    latest_readings = history[0]
    return latest_readings
