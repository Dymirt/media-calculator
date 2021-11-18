from tkinter import *
from tkinter.ttk import *
from util import history, models

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

# PAYMENTS
total_payment = 0

# Readings
cold_water = models.reading(cold_water_price)
hot_water = models.reading(hot_water_price)
electricity = models.reading(electricity_price, electricity_abonament)


# UPDATE ACTUAL READINGS DONE
def get_readings():
    cold_water.set_actual(float(cold_water_entry.get()))
    hot_water.set_actual(float(hot_water_entry.get()))
    electricity.set_actual(float(electricity_entry.get()))


# Payment Calculation
def payment(latest, actual, price, abonament_price):
    consumption = actual - latest
    payment = consumption * price
    if abonament_price > 0:
        payment += abonament_price
    return payment


# UPDATE ACTUAL PAYMENTS GLOBAL VARIABLES
def calculate_payments():

    get_readings()
    latest_readings_update()

    global total_payment
    total_payment = cold_water.payment + hot_water.payment + electricity.payment


# UPDATE LATEST READING DONE
def latest_readings_update():
    global latest_reading
    latest_reading = history.get_latest_readings()

    cold_water.set_latest(latest_reading["Cold water"])
    hot_water.set_latest(latest_reading["Hot water"])
    electricity.set_latest(latest_reading["Electricity"])


# Append actual data to history
def append_history():
    calculate_payments()
    history.append_history(
        cold_water.actual, cold_water.payment,
        hot_water.actual, hot_water.payment,
        electricity.actual, electricity.payment,
        total_payment
    )
    latest_reading_output()


# CLEAR HISTORY
def clear():
    history.clear_history()
    latest_reading_output()


# Dynamicly generated labels for reading names
def latest_reading_labels(start_row):
    latest_reading_list = list(latest_reading)
    for item in range(2, len(latest_reading_list) - 1, 2):
        cols = f"Latest {latest_reading_list[item]} reading is:"
        Label(window, text=cols, justify='left',
              width=30) .grid(column=0, row=start_row)
        start_row += 1


# Update information on LATEST READING BLOCK
def latest_reading_output():
    latest_readings_update()
    if latest_reading["Month"] == 0:
        dat.set("LATEST READINGS")
    else:
        dat.set(
            f"LATEST READINGS FROM {latest_reading['Month']}/20{latest_reading['Year']}")
    label_cold_water_latest_reading.set(f"{cold_water.latest} Cubic metre")
    label_hot_water_latest_reading.set(f"{hot_water.latest} Cubic metre")
    label_electricity_latest_reading.set(f"{electricity.latest} KW/h")


window = Tk()

# Tkinter window properties
window.title("Media Calculator")
window.geometry("1000x200")
output = StringVar()
label_cold_water_latest_reading = StringVar()
label_hot_water_latest_reading = StringVar()
label_electricity_latest_reading = StringVar()
dat = StringVar()

# LATEST READINGS BLOCK **********************************************
latest_reading_output()

latest_readings_start_column = 0
latest_readings_start_row = 0
Label(window, textvariable=dat) .grid(column=latest_readings_start_column,
                                      row=latest_readings_start_row, columnspan=2)

latest_readings_start_row += 1
latest_reading_labels(latest_readings_start_row)

Label(window, textvariable=label_cold_water_latest_reading, justify='left', width=20) .grid(
    column=latest_readings_start_column + 1, row=latest_readings_start_row)

latest_readings_start_row += 1
Label(window, textvariable=label_hot_water_latest_reading, justify='left', width=20) .grid(
    column=latest_readings_start_column + 1, row=latest_readings_start_row)

latest_readings_start_row += 1
Label(window, textvariable=label_electricity_latest_reading, justify='left', width=20) .grid(
    column=latest_readings_start_column + 1, row=latest_readings_start_row)

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
       command=calculate_payments) .grid(row=input_row, column=input_column)

window.mainloop()
