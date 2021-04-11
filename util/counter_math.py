# Payment Calculation
def payment_counter(before,after,price,subscribe_price):
    consumption = after - before
    payment = consumption * price
    if subscribe_price > 0:
        payment += subscribe_price
    return payment
