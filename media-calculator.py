import datetime
import json
from itertools import islice
from tkinter import *


def main():
    
    cold_water_price = 9.85
    hot_water_price = cold_water_price + 20.61
    electricity_price = 0.481053
    electricity_abonament = 21.98

    history = history_r()
    if len(history) > 0:
        last_counters = history[0]
    else:
        last_counters = {'Date': 0, 'Cold water': 0, 'Hot water' : 0, 'Electricity': 0, 'Total Money': 0}

    try:
        cold_water_after = float(cold_water_entry.get())
        hot_water_after = float(hot_water_entry.get())
        electricity_after = float(electricity_entry.get())
    except Exception as e:
        print(e)

    cold_water_payment = cold_wather_counter(last_counters["Cold water"], cold_water_after, cold_water_price)
    hot_water_payment = hot_water_counter(last_counters["Hot water"], hot_water_after, hot_water_price)
    electricity_payment = electricity_counter(last_counters["Electricity"], electricity_after, electricity_price, electricity_abonament)
    total_payment = cold_water_payment + hot_water_payment + electricity_payment

    history_w(round(cold_water_after, 2), round(hot_water_after, 2), round(electricity_after, 2), round(total_payment,2))


#Cold water counter
def cold_wather_counter(cold_water_before, cold_water_after, cold_water_price):
    cold_water_consumption = cold_water_after - cold_water_before
    cold_water_payment = cold_water_consumption * cold_water_price
    return cold_water_payment


# Hot water conter
def hot_water_counter(hot_water_before, hot_water_after, hot_water_price):
    hot_water_consumption = hot_water_after - hot_water_before
    hot_water_payment = hot_water_consumption * hot_water_price
    return hot_water_payment


# Electricity counter
def electricity_counter(electricity_before, electricity_after, electricity_price, electricity_abonament):
    electricity_consumption = electricity_after - electricity_before
    electricity_payment = electricity_consumption * electricity_price
    electricity_payment += electricity_abonament
    return electricity_payment

    
# Change result lable 
def result_label():
    result["text"] = ""
    history = history_r()
    if len(history) > 0:
        last_counters = history[0]
        result["text"] = last_counters
    window.after(1000, result_label)


# Clear history 
def history_c():
    try:
        with open("history.txt", "w") as f:
            pass
    except Exception as e:
        print(e)


# Save data to the history file
def history_w(cold_water, hot_water, electricity, total_money):
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
def history_r():
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

window = Tk()

window.title("Media Calculator")
window.geometry("1000x200")
# Labels
Label(window, text="Cold water counter") .grid(row=0, column=0)
Label(window, text="Hot water counter") .grid(row=1, column=0)
Label(window, text="Electricity counter") .grid(row=2, column=0)

#Input values
cold_water_entry = Entry(window, width=10)
cold_water_entry.grid(row=0, column=1)

hot_water_entry = Entry(window, width=10)
hot_water_entry.grid(row=1, column=1)

electricity_entry = Entry(window, width=10)
electricity_entry.grid(row=2, column=1)

#Submit Button
Button(window, text="CONFIRM", width=20, highlightbackground="Black", command=main) .grid(row=3, column=1)
Button(window, text="Clear history", width=10, highlightbackground="Black", command=history_c) .grid(row=5, column=1)

result = Label(window, text='') 
result.grid(row=4, column=0)

window.after(1, result_label)


window.mainloop()