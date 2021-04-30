from tkinter import *
from tkinter.ttk import *
from util import history

# Cold water pricelist
cold_water_price = 9.85
cold_water_abonament = 0

# Hot water priselist
hot_water_price = cold_water_price + 20.61
hot_water_abonament = 0

# Electricity pricelist
electricity_price = 0.481053
electricity_abonament = 21.98

# Latest readings from history
latest_reading = []
cold_water_latest_reading = 0
hot_water_latest_reading = 0
electricity_latest_reading = 0

# Actual readings
cold_water_actual_reading = 0
hot_water_actual_reading = 0
electricity_actual_reading = 0

# Actual payments
cold_water_payment = 0
hot_water_payment = 0
electricity_payment = 0
total_payment = 0


# Get readings from user update GLOBAL VARIABLE
def get_counters():
    global cold_water_actual_reading
    global hot_water_actual_reading
    global electricity_actual_reading
    try:
        cold_water_actual_reading = float(cold_water_entry.get())
        hot_water_actual_reading = float(hot_water_entry.get())
        electricity_actual_reading = float(electricity_entry.get())
    except Exception as e:
        print(e)


# Payment Calculation
def payment(latest, actual, price, abonament_price):
    consumption = actual - latest
    payment = consumption * price
    if abonament_price > 0:
        payment += abonament_price
    return payment


# UPDATE GLOBAL VARIABLES
def calculate_paymants():

    # GLOBAL VARIABLES
    global latest_reading
    global cold_water_latest_reading
    global hot_water_latest_reading
    global electricity_latest_reading
    global cold_water_payment
    global hot_water_payment
    global electricity_payment
    global total_payment

    # Get actual readings from user
    get_counters()

    # Update latest readings
    latest_readings_update()

    # Cold water paymant calculation update GLOBAL VARIABLE
    cold_water_payment = payment(cold_water_latest_reading, cold_water_actual_reading,
                                 cold_water_price, cold_water_abonament)

    # Hot water paymant calculation update GLOBAL VARIABLE
    hot_water_payment = payment(hot_water_latest_reading, hot_water_actual_reading,
                                hot_water_price, hot_water_abonament)

    # Electricity paymant calculation update GLOBAL VARIABLE
    electricity_payment = payment(electricity_latest_reading, electricity_actual_reading,
                                  electricity_price, electricity_abonament)

    # Total Payment calculation update GLOBAL VARIABLE
    total_payment = cold_water_payment + hot_water_payment + electricity_payment


def latest_readings_update():
    global latest_reading
    global cold_water_latest_reading
    global hot_water_latest_reading
    global electricity_latest_reading

    latest_reading = history.get_latest_readings()
    cold_water_latest_reading = latest_reading["Cold water"]
    hot_water_latest_reading = latest_reading["Hot water"]
    electricity_latest_reading = latest_reading["Electricity"]


# Append actual data to history
def append_history():
    calculate_paymants()
    history.append_history(
        round(cold_water_actual_reading, 2),
        round(cold_water_payment, 2),
        round(hot_water_actual_reading, 2),
        round(hot_water_payment, 2),
        round(electricity_actual_reading, 2),
        round(electricity_payment, 2),
        round(total_payment, 2)
    )
    latest_reading_output()


def clear():
    history.clear_history()
    latest_reading_output()


def latest_reading_labels(start_row):
    latest_readings_update()
    latest_reading_list = list(latest_reading)
    for item in range(2, len(latest_reading_list) - 1, 2):
        cols = f"Latest {latest_reading_list[item]} reading is:"
        Label(window, text=cols, justify='left',
              width=30) .grid(column=0, row=start_row)
        start_row += 1


def latest_reading_output():
    latest_readings_update()
    if latest_reading["Month"] == 0:
        dat.set("LATEST READINGS")
    else:
        dat.set(
            f"LATEST READINGS FROM {latest_reading['Month']}/20{latest_reading['Year']}")
    co.set(f"{round(cold_water_latest_reading, 2)} Cubic metre")
    ho.set(f"{round(hot_water_latest_reading, 2)} Cubic metre")
    el.set(f"{round(electricity_latest_reading, 2)} KW/h")


window = Tk()

# TKinter window properties
window.title("Media Calculator")
window.geometry("1000x200")
window.configure(background='#ececeb')
output = StringVar()
co = StringVar()
ho = StringVar()
el = StringVar()
dat = StringVar()

# LATEST READINGS BLOCK **********************************************
latest_readings_start_column = 0
latest_readings_start_row = 0
Label(window, textvariable=dat) .grid(column=latest_readings_start_column,
                                      row=latest_readings_start_row, columnspan=2)

latest_readings_start_row += 1
latest_reading_labels(latest_readings_start_row)

Label(window, textvariable=co, justify='left', width=20) .grid(
    column=latest_readings_start_column + 1, row=latest_readings_start_row)

latest_readings_start_row += 1
Label(window, textvariable=ho, justify='left', width=20) .grid(
    column=latest_readings_start_column + 1, row=latest_readings_start_row)

latest_readings_start_row += 1
Label(window, textvariable=el, justify='left', width=20) .grid(
    column=latest_readings_start_column + 1, row=latest_readings_start_row)

latest_reading_output()

latest_readings_start_row += 1
Button(window, text="Clear history", width=10,
       command=clear) .grid(column=latest_readings_start_column, row=latest_readings_start_row, columnspan=2)


# CALCULATE BLOCK *****************************************************

# Position
calculate_start_column = 2
calculate_start_row = 0

# Labels
label_row = calculate_start_row

Label(window, text="INPUT YOUR ACTUAL READINGS") .grid(
    row=label_row, column=calculate_start_column, columnspan=2)
label_row += 1
Label(window, text="Cold water counter", justify='left', width=20) .grid(
    row=label_row, column=calculate_start_column)
label_row += 1
Label(window, text="Hot water counter", justify='left', width=20) .grid(
    row=label_row, column=calculate_start_column)
label_row += 1
Label(window, text="Electricity counter", justify='left', width=20) .grid(
    row=label_row, column=calculate_start_column)

# Input values
input_row = calculate_start_row + 1
input_column = calculate_start_column + 1

cold_water_entry = Entry(window, width=10)
cold_water_entry.grid(row=input_row, column=input_column)
input_row += 1
hot_water_entry = Entry(window, width=10)
hot_water_entry.grid(row=input_row, column=input_column)
input_row += 1
electricity_entry = Entry(window, width=10)
electricity_entry.grid(row=input_row, column=input_column)

# Submit Button
input_row += 1
Button(window, text="Save calculation", width=20,
       command=append_history) .grid(row=input_row, column=calculate_start_column)
Button(window, text="Calculate Payments", width=20,
       command=calculate_paymants) .grid(row=input_row, column=input_column)

window.mainloop()
