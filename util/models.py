class reading:

    def __init__(self, price, abonament=0):
        self.price = price
        self.abonament = abonament
        self.latest = 0
        self.actual = 0
        self.payment = 0

    def set_actual(self, actual):
        self.actual = actual
        self.calculate_payment(self.consumption())

    def set_latest(self, latest):
        self.latest = latest
        self.calculate_payment(self.consumption())

    def calculate_payment(self, consumption):
        payment = consumption * self.price
        self.payment = payment + self.abonament

    def consumption(self):
        return self.actual - self.latest
