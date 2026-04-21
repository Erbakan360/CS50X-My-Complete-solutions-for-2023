# TODO

# Using cs50 library to get 'get_float' function
from cs50 import get_float

# function to calculate


def calculate(foo, X):
    # Initialize Counter variable
    bar = 0
    # Loop through the given dollar amount until the current coin can no longer be subtracted
    while X <= round(foo, 3):
        # Subract change
        foo -= X
        # Increase counter
        bar += 1
        # round of dollar value to 3 decimel places
        foo = round(foo, 3)
    # return counter
    return bar


# // Ask how many Dollars the customer is owed
while (True):
    Dollars = get_float("Change owed: ")
    if (Dollars > 0):
        break
# Initialization of all relevant values
quarter = 0.25
dimes = 0.1
nickels = 0.05
pennies = 0.01
Counter = 0  # To keep track of how many of each coin has been used
coins = 0  # To keep track of the total coins have been used


# Calculate how many quarters required
Counter = calculate(Dollars, quarter)
Dollars = Dollars - (Counter * quarter)
coins += Counter

# Calculate how many quarters required
Counter = calculate(Dollars, dimes)
Dollars = Dollars - (Counter * dimes)
coins += Counter

# Calculate how many quarters required
Counter = calculate(Dollars, nickels)
Dollars = Dollars - (Counter * nickels)
coins += Counter

# Calculate how many quarters required
Counter = calculate(Dollars, pennies)
Dollars = Dollars - (Counter * pennies)
coins += Counter

# OUTPUT
print(coins)
