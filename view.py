from tkinter import *
from tkinter.ttk import *
from util import models, database
from guppy import hpy

h = hpy()


window = Tk()
window.title('Utility payment')
window.geometry("1000x200")
# database.set_utilities()
all_utilities = models.ShowAllUtilities(text="All utilities")
add_utility = models.AddUtilityFrame(text="Add Utility")
d = models.AddUtilityValues()

# Menu configuration
menu_bar = Menu(window)
window.config(menu=menu_bar)
#
file_menu = Menu(menu_bar)
menu_bar.add_cascade(
    label="Utility",
    menu=file_menu
)
# Utility menu options
file_menu.add_command(
    label="Show utilities",
    command=all_utilities.switch
)
file_menu.add_command(
    label="Add Utility",
    command=add_utility.switch
)

# TODO calculate consumption and payment
file_menu.add_command(
    label="Calculate",
    command=d.switch
)

window.mainloop()
print(h.heap())
