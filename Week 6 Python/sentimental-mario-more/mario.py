# TODO.

Height = 0
Space = 0
Hashes = 0
Valid = False

# Loops until a Valid value is input
while (Valid == False):
    # Inputs the Value from the user
    Height = input("Height: ")
    # Confirms if user has input a value
    if Height == None:
        Valid = False
    # if a Value is present
    elif Height != None:
        # Checks if the Value is numeric using .isnumeric() function
        if Height.isnumeric() == False:
            Valid = False
        # if the value is numeric it checks if it is in the Valid range
        elif int(Height) > 0 and int(Height) < 9:
            Valid = True
            # Converts Hieght into Int
            Height = int(Height)

# Loop for Pyramid
for i in range(1, Height + 1):
    # initialization of number of Spaces
    Space = Height - i
    # Initialization for Number of "Bricks"
    Hashes = i
    # 
    if Space != 0 and Space < 8:
        while (Space > 0):
            print(" ", end="")
            Space -= 1
    while (Hashes > 0):
        print("#", end="")
        Hashes -= 1

    print("  ", end="")

    Hashes = i
    while (Hashes > 0):
        print("#", end="")
        Hashes -= 1

    print()