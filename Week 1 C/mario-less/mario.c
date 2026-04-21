#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Initialization/Creation of Variables
    int (Height);
    int (Space);
    int (Hashes);

    // Get value of Height
    do
    {
        Height = get_int("Height: ");
    }
    while ((Height > 8) || (Height < 1));

    // Loop for pyramid
    for (int i = 1; i <= Height; i++)
        {
            // Amount of Spaces before each brick
            Space = Height - i;
            // Amount of bricks per row
            Hashes = Height - Space;
            //
            if ((Space != 0) && (Space < 8))
            {
                // Loop for Space(s) in a row
                do
                {
                    printf(" ");
                    Space--;
                }
                while (Space > 0);
            }
            // Loop for brick(s) in a row
            do
            {
                printf("#");
                Hashes--;
            }
            while (Hashes > 0);
        printf("\n");
        }
}