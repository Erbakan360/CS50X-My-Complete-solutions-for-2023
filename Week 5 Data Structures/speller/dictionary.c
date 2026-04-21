// Implements a dictionary's functionality
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <stdbool.h>

#include "dictionary.h"


// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;
int Counts = 0; // Creates a variable to count the number of words in the dictionary

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    int hashNum = hash(word);
    node *Checker = table[hashNum];

    while (Checker != NULL)
    {
        // Compare words
        if (strcasecmp(Checker->word, word) == 0)
        {
            return true;
        }
        // Move to next node
        Checker = Checker->next;
    }

    return false;
}

// Hashes word to a number
int C = 0;
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    return toupper(word[0]) - 'A';
}
// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open the dictionary file
    FILE *file = fopen(dictionary, "r");
    // Check if return value is NULL
    if (file == NULL)
    {
        return false;
    }
    //Read strings from
    char Words[LENGTH + 1];
    while (fscanf(file, "%s", Words) != EOF)
    {
        // Create a new node for each word
        // Use malloc
        node *Tmp = malloc(sizeof(node));
        // Check if the return value is NULL
        if (Tmp == NULL)
        {
            fclose(file);
            return false;
        }
        // Copy word into node
        strcpy(Tmp->word, Words);

        //Use hash function
        int hashNum = hash(Words);

        // chech if the head is pointing to NULL
        if (table[hashNum] == NULL)
        {
            // Point Tmp to NULL
            Tmp ->next = NULL;
        }
        else
        {
            // Otherwise, point temp to the first node of the linked list
            Tmp->next = table[hashNum];
        }

        // Point the header to temp
        table[hashNum] = Tmp;

        Counts += 1;
    }
    // Close the file
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return Counts;
}

void freefunc(node *n)
{
    if (n->next != NULL)
    {
        freefunc(n->next);
    }
    free(n);
}
// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
        if (table[i] != NULL)
        {
            freefunc(table[i]);
        }
    return true;
}
