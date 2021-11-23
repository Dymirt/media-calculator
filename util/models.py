import datetime

from . import database
from tkinter import *
from tkinter.ttk import *


class Utility:
    def __init__(self, name, price, subscription_price=0, symbol="units", curency="zł"):
        self.name = name
        self.price = price
        self.subscription_price = subscription_price
        self.symbol = symbol
        self.latest = 0
        self.actual = 0
        self.payment: int
        self.history_value: int
        self.curency = curency

    def __set_name(self):
        pass

    def set_actual(self, actual):
        self.actual = actual
        self.calculate_payment(self.consumption())

    def set_latest(self, latest):
        self.latest = latest
        self.calculate_payment(self.consumption())

    def calculate_payment(self, consumption):
        self.payment = (consumption * self.price) + self.subscription_price

    def consumption(self):
        return self.actual - self.latest

    def chek_consumption(self, after):
        consumption = self.history_value - after
        if consumption > 0:
            return consumption
        else:
            return 0

    def price_list(self):
        return f"{self.name} price {self.price} {self.curency}/{self.symbol}" \
               f" + subscription {self.subscription_price} {self.curency}/month"


class Switchable(Tk):
    def switch(self):
        if not self.winfo_viewable():
            self.pack()
        else:
            self.pack_forget()


class ShowAllUtilities(LabelFrame, Switchable):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.utilities = database.get_all_utilities()
        self.output()

    def output(self):
        if not self.utilities:
            Label(self, text="No utilities added").grid()
            Button(self, text="Add Utility").grid()
        else:
            row = 1
            for i in self.utilities:
                for j in range(len(i)):
                    Label(self, text=i[j]).grid(row=row, column=j)
                row += 1
            Button(self, text="CLOSE", command=self.switch).grid(row=row, column=1)


class AddUtilityFrame(LabelFrame, Switchable):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.name = StringVar()
        self.symbol = StringVar()
        self.price = DoubleVar()
        self.subscription_price = DoubleVar()
        # Dictionary of Utility properties
        self.utility_property = {
            "Name": self.name,
            "Symbol": self.symbol,
            "Price": self.price,
            "SubscriptionPrice": self.subscription_price
        }

        self.output()

    def output(self):
        row = 0
        for item in self.utility_property:
            Label(self, text=item).grid(column=0, row=row)
            Entry(self, textvariable=self.utility_property.get(item)).grid(column=1, row=row)
            row = row + 1
        Button(self, text="ADD UTILITY", command=self.create_new_utility).grid(column=1, row=row)
        Button(self, text="CLOSE", command=self.switch).grid(column=0, row=row)

    def create_new_utility(self):
        utility_data = []
        for i in self.utility_property:
            utility_data.append(self.utility_property.get(i).get())
            self.utility_property.get(i).set("")
        print(utility_data)
        database.add_utility(tuple(utility_data))


class AddUtilityValues(LabelFrame, Switchable):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.set_utility_combobox = None
        self.set_utility_button = None

        # Date
        self.date = StringVar()
        self.date.set(self.set_date())
        self.utilityId = IntVar()

        self.utility_dict = database.get_all_utility_name()

        self.utilityName = ""

        self.price = DoubleVar()
        self.subscription_price = DoubleVar()
        self.history_value = DoubleVar()
        self.value = DoubleVar()
        self.consumption = DoubleVar()
        self.payment = DoubleVar()

        # Help
        self.get_utility_name = StringVar()

        self.select_utility()

    @staticmethod
    def set_date():
        current_date = datetime.datetime.now()
        return f"{current_date.strftime('%m')}/{current_date.strftime('%y')}"

    def get_price(self):
        prices = database.get_values_by_name(self.utilityName)
        self.price.set(prices[0])
        self.subscription_price.set(prices[1])

    def select_utility(self):
        Label(self, text="Select Utility").grid()
        name_list = []
        for i in self.utility_dict:
            name_list.append(self.utility_dict.get(i))
        Combobox(self, values=name_list, textvariable=self.get_utility_name).grid()
        Button(self, text="Select", command=self.set_utility_name).grid()

    def output(self):
        Entry(self, textvariable=self.date).grid()
        Entry(self, textvariable=self.price).grid()
        Entry(self, textvariable=self.subscription_price).grid()
        Entry(self, textvariable=self.history_value).grid()
        Entry(self, textvariable=self.value).grid()
        Button(self, text="Calculate consumption", command=self.calculate_consumption).grid()
        Entry(self, textvariable=self.consumption).grid()

        Button(self, text="Calculate payment", command=self.calculate_payment).grid()
        Entry(self, textvariable=self.payment).grid()
        Button(self, text="Add Value").grid()
        print(self.grid_slaves())

    def set_utility_name(self):
        self.utilityName = self.get_utility_name.get()
        self.get_price()
        self.output()

    def calculate_consumption(self):
        self.consumption.set(self.value.get() - self.history_value.get())

    def calculate_payment(self):
        consumption = float(self.consumption.get())
        price = float(self.price.get())
        s_p = float(self.subscription_price.get())
        self.payment.set(consumption * price + s_p)






