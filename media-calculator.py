from tkinter import *
from util import history, counter_math


def main():
    # Cold water pricelist 
    cold_water_price = 9.85
    cold_water_subscribe = 0
    
    # Hot water priselist
    hot_water_price = cold_water_price + 20.61
    hot_water_subscribe = 0

    # Electricity pricelist
    electricity_price = 0.481053
    electricity_subscribe = 21.98

    history_dict = history.read_history()
    if len(history_dict) > 0:
        last_counters = history_dict[0]
    else:
        last_counters = {'Date': 0, 'Cold water': 0, 'Hot water' : 0, 'Electricity': 0, 'Total Money': 0}

    try:
        cold_water_after = float(cold_water_entry.get())
        hot_water_after = float(hot_water_entry.get())
        electricity_after = float(electricity_entry.get())
    except Exception as e:
        print(e)

    cold_water_payment = counter_math.payment_counter(last_counters["Cold water"], cold_water_after, cold_water_price,cold_water_subscribe)
    hot_water_payment = counter_math.payment_counter(last_counters["Hot water"], hot_water_after, hot_water_price,hot_water_subscribe)
    electricity_payment = counter_math.payment_counter(last_counters["Electricity"], electricity_after, electricity_price, electricity_subscribe)
    
    total_payment = cold_water_payment + hot_water_payment + electricity_payment

    history.write_history(round(cold_water_after, 2), round(hot_water_after, 2), round(electricity_after, 2), round(total_payment,2))

    
# Change result lable 
def result_label():
    result["text"] = ""
    history_dict = history.read_history()
    if len(history_dict) > 0:
        last_counters = history_dict[0]
        result["text"] = last_counters
    window.after(1000, result_label)



window = Tk()

# TKinter window properties
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
Button(window, text="Clear history", width=10, highlightbackground="Black", command=history.clear_history) .grid(row=5, column=1)

#Result Label
result = Label(window, text='') 
result.grid(row=4, column=0)
window.after(1, result_label)


window.mainloop()