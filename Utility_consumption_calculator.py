import json
from tkinter import *
from tkinter.ttk import *
from util import history, models

# Cold water pricelist
cold_water_price = 9.85
cold_water_abonament = 0

# Hot water priselist
hot_water_price = 9.85 + 20.61
hot_water_abonament = 0

# Electricity pricelist
electricity_price = 0.481053
electricity_abonament = 21.98

# Latest readings from history
latest_reading = []

# PAYMENTS
total_payment = 0

# Readings
cold_water = models.Utility(cold_water_price)
hot_water = models.Utility(hot_water_price)
electricity = models.Utility(electricity_price, electricity_abonament)


# UPDATE ACTUAL READINGS DONE
def get_readings():
    cold_water.set_actual(float(cold_water_entry.get()))
    hot_water.set_actual(float(hot_water_entry.get()))
    electricity.set_actual(float(electricity_entry.get()))


# Payment Calculation
def payment(latest, actual, price, subscription_price):
    consumption = actual - latest
    payment = consumption * price
    if subscription_price > 0:
        payment += subscription_price
    return payment


# UPDATE ACTUAL PAYMENTS GLOBAL VARIABLES
def calculate_payments():
    get_readings()
    latest_readings_update()

    global total_payment
    total_payment = cold_water.payment + hot_water.payment + electricity.payment
    p = total_payment
    output.set(p)


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


# Dynamicly generated labels for Utility names
def latest_reading_labels():
    start_row = 0
    for item in latest_reading:
        Label(window, text=item + ":", justify='left', width=30) \
            .grid(column=0, row=start_row)
        Label(window, text=latest_reading[item], justify='left', width=30) \
            .grid(column=1, row=start_row)
        start_row += 1


# Update information on LATEST READING BLOCK
def latest_reading_output():
    latest_readings_update()
    latest_reading_labels()
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
latest_reading_frame = LabelFrame(window, text="Latest").grid()

latest_readings_start_column = 0
latest_readings_start_row = 0
Label(window, textvariable=dat).grid(row=0, columnspan=2, in_=latest_reading_frame)

latest_readings_start_row += 1
latest_reading_labels()

Label(window, textvariable=label_cold_water_latest_reading, justify='left', width=20).grid(
    column=latest_readings_start_column + 1, row=latest_readings_start_row, in_=latest_reading_frame)

latest_readings_start_row += 1
Label(window, textvariable=label_hot_water_latest_reading, justify='left', width=20).grid(
    column=latest_readings_start_column + 1, row=latest_readings_start_row)

latest_readings_start_row += 1
Label(window, textvariable=label_electricity_latest_reading, justify='left', width=20).grid(
    column=latest_readings_start_column + 1, row=latest_readings_start_row)

latest_readings_start_row += 1
Button(window, text="Clear history", width=10,
       command=clear).grid(column=latest_readings_start_column, row=latest_readings_start_row, columnspan=2)

# CALCULATE BLOCK *****************************************************
# Position
calculate_start_column = 2
calculate_start_row = 0

# Labels
label_row = calculate_start_row

Label(window, text="INPUT YOUR ACTUAL READINGS").grid(
    row=label_row, column=calculate_start_column, columnspan=2)
label_row += 1
Label(window, text="Cold water counter", justify='left', width=20).grid(
    row=label_row, column=calculate_start_column)
label_row += 1
Label(window, text="Hot water counter", justify='left', width=20).grid(
    row=label_row, column=calculate_start_column)
label_row += 1
Label(window, text="Electricity counter", justify='left', width=20).grid(
    row=label_row, column=calculate_start_column)

Label(window, textvariable=output).grid()

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
       command=append_history).grid(row=input_row, column=calculate_start_column)
Button(window, text="Calculate Payments", width=20,
       command=calculate_payments).grid(row=input_row, column=input_column)

######################################################################################
#
######################################################################################

# New Utility variables
new_utility_name = StringVar()
new_utility_meter = StringVar()
new_utility_price = DoubleVar()
new_utility_subscription = DoubleVar()

new_utility_dict = {
    "Name": new_utility_name,
    "Meter": new_utility_meter,
    "Price": new_utility_price,
    "Subscription": new_utility_subscription
}


# Function to support frame
def new_utility_frame():
    if add_utility_frame.winfo_viewable():
        add_utility_frame.grid_remove()
    else:
        add_utility_frame.grid()
        add_utility_menu_button.grid_remove()


# Menu button ADD UTILITY
add_utility_menu_button = Button(window, text="Add Utility", command=new_utility_frame)
add_utility_menu_button.grid()

# ADD UTILITY FIELDS
add_utility_frame = LabelFrame(window, text="Add new utility")
row = 0
for i in new_utility_dict:
    i = Label(window, text=i).grid(column=0, row=row, in_=add_utility_frame)
    Entry(window, textvariable=dict[i]).grid(column=1, row=row, in_=add_utility_frame)
    row = row + 1
Button(window, text="Add utility").grid(columnspan=2, in_=add_utility_frame)

window.mainloop()
