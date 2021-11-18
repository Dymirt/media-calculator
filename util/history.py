import datetime
import json

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

    history = {
        "Month": current_date.strftime("%m"),
        "Year": current_date.strftime("%y"),
        "Cold water": round(cold_water, 2),
        "Cold water payment": round(cold_water_payment, 2),
        "Hot water": round(hot_water, 2),
        "Hot water payment": round(hot_water_payment, 2),
        "Electricity": round(electricity, 2),
        "Electricity payment": round(electricity_payment, 2),
        "Total Payment": round(total_payment, 2)
    }

    # Add JSON data to txt file
    with open("history.txt", "a") as f:
        f.write("\n")
        f.write(json.dumps(history))


# Read history from file. if history is empty append zeros to file
def get_history():
    history = []
    try:
        with open('history.txt') as f:
            for i in f.readlines():
                history.append(json.loads(i.replace("'", "\"")))
    except Exception as e:
        print(e)
        # Create history.txt
        clear_history()
        # Return history using recursion
        history = get_history()
    return history


# Return latest counters from history.
def get_latest_readings():
    return get_history()[-1]
