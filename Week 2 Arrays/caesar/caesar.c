#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>

int Rotate(char Plain, int K);

int main(int argc, string argv[])
{
    // Confirm key is provided
    if (argc != 2)
    {
        printf("Insert as follows: ./caesar Key (where key needs to be integer)\n");
        return 1;
    }

    //Check if key is numericaly
    for (int i = 0; i < strlen(argv[1]); i++)
        if (isdigit(argv[1][i]) == false)
        {
            printf("Insert as follows: ./caesar Key. where key needs to be integer\n");
            return 1;
        }
    // Convert key to integer
    int Key = atoi(argv[1]);

    // Get plaintext
    string plaintext = get_string("Input Plaintext: ");

    printf("Ciphertext: ");
    for (int j = 0; j < strlen(plaintext); j++)
    {
        char Ciphertext = Rotate(plaintext[j], Key);
        printf("%c", Ciphertext);
    }
    printf("\n");
}

int Rotate(char Plain, int K)
{
    char C = 'k';
    if (isupper(Plain))
    {
        C = (Plain + K -65) % 26 + 65;
    }
    else if (islower(Plain))
    {
        C = (Plain + K - 97)  % 26 + 97;
    }
    else
    {
        C = Plain;
    }
    return C;
}