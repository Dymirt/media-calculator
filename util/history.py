import datetime
import json
from itertools import islice

# Clear history 
def clear_history():
    try:
        with open("history.txt", "w") as f:
            pass
    except Exception as e:
        print(e)


# Save data to the history file
def write_history(cold_water, hot_water, electricity, total_money):
    # Corrent date
    current_date = datetime.datetime.now()
    month = int(current_date.strftime("%m"))
    yaear = int(current_date.strftime("%y"))

    # Create JSON
    data = "{"
    data += f"\'Month\':{month},"
    data += f" \'Year\':{yaear},"
    data += f" \'Cold water\':{cold_water},"
    data += f" \'Hot water\':{hot_water},"
    data += f" \'Electricity\':{electricity},"
    data += f" \'Total Money\':{total_money}"
    data += "}"

    # Add JSON data to txt file
    with open("history.txt", "a") as f:
        print(data, file=f)

# Read history from file
def read_history():
    history = []
    try:
        with open('history.txt') as f:
            for line in islice(f,0,None):
                json_acceptable_string = line.replace("'", "\"")
                d = json.loads(json_acceptable_string)
                history.insert(0, d)
    except Exception as e:
        print(e)
    return history