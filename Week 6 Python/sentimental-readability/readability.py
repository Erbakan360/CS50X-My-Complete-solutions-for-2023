# TODO

from cs50 import get_string

# Declare variable for users Text
Text = get_string("Insert text: ")
Words = 1
Sentences = 0
Letters = 0

# Initializes variables i, Sentences, Letters & Words. Loops through the string of text inserted by user.
for i in range(len(Text)):
    # Checks if the current Character is a Space
    if ((Text[i] >= chr(97) and Text[i] <= chr(123)) or (Text[i] >= chr(65) and Text[i] <= chr(91))):
        # Increments variable for Number of Letters
        Letters += 1

    # Checks if the current Character is a "." , "!" or "?"
    elif (Text[i] == "." or Text[i] == "!" or Text[i] == "?"):
        # Increments variable for Number of Sentences
        Sentences += 1

    # Checks if the current Character is between the letter a to z or A to Z
    elif (Text[i] == " "):
        # Increments variable for Number of Words
        Words += 1

# Calculation of the Coleman-Liau index
L = Letters / Words * 100
S = Sentences / Words * 100
Solve = float(0.0588 * L - 0.296 * S - 15.8)
print(Solve)
# Rounds of Coleman-Liau index
index = round(Solve)

if (index < 1):
    # For grades below 1
    print("Before Grade 1\n")
elif (index >= 16):
    # For grade 16 and above
    print("Grade 16+")
else:
    # For grades Between 1 and 15
    print("Grade", index)