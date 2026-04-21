#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

int main(void)
{
    // Declare variable for users Text
    string Text = get_string("Insert text: ");

     // Declare variable for Number of Words

    int (Sentences); // Declare variable for Number of Sentences

    int (Letters); // Declare variable for Number of Letters

    int (i); // Declare variable for for loop

    int (Characters) = strlen(Text); // Declare variable for Number of Characters

    // Initializes variables i, Sentences, Letters & Words. Loops through the string of text inserted by user.
    for (i = 0, Sentences = 0, Words = 1, Letters = 0; i < Characters; i++)
        // Checks if the current Character is a Space
        if (Text[i] == ' ')
        {
            // Increments variable for Number of Words
            Words++;
        }
    // Checks if the current Character is a '.', '!' or '?'
        else if (Text[i] == '.' || Text[i] == '!' || Text[i] == '?')
        {
            // Increments variable for Number of Sentences
            Sentences++;
        }
    // Checks if the current Character is between the letter 'a' to 'z' or 'A' to 'Z'
        else if ((Text[i] >= 'a' && Text[i] <= 'z') || (Text[i] >= 'A'  && Text[i] <= 'Z'))
        {
            // Increments variable for Number of Letters
            Letters++;
        }

    // Calculation of the Coleman-Liau index
    float Solve = (0.0588 * Letters / Words * 100) - (0.296 * Sentences / Words * 100) - 15.8;

    // Rounds of Coleman-Liau index
    int index = round(Solve);

    if (index < 1)
    {
        // For grades below 1
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        // For grade 16 and above
        printf("Grade 16+\n");
    }
    else
    {
        // For grades Between 1 and 15
        printf("Grade %i\n", index);
    }
}