#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// Hash table size
#define HASH_TABLE_SIZE 65536

// Hash table
node *table[HASH_TABLE_SIZE];

// Hash function
unsigned int hash(const char *word)
{
    unsigned int hash_value = 0;
    for (int i = 0; word[i] != '\0'; i++)
    {
        hash_value = (hash_value << 2) ^ word[i];
    }
    return hash_value % HASH_TABLE_SIZE;
}

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Convert word to lowercase
    char lowercase_word[LENGTH + 1];
    for (int i = 0; word[i] != '\0'; i++)
    {
        lowercase_word[i] = tolower(word[i]);
    }
    lowercase_word[strlen(word)] = '\0';

    // Hash the word to get the index in the table
    unsigned int index = hash(lowercase_word);

    // Traverse the linked list at the index
    node *cursor = table[index];
    while (cursor != NULL)
    {
        // Compare lowercase word with dictionary word
        if (strcmp(lowercase_word, cursor->word) == 0)
        {
            return true; // Word found
        }
        cursor = cursor->next;
    }

    return false; // Word not found
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open dictionary file
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        printf("Could not open %s.\n", dictionary);
        return false;
    }

    // Read each word from file
    char word[LENGTH + 1];
    while (fscanf(file, "%s", word) != EOF)
    {
        // Create a new node for the word
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            fclose(file);
            return false;
        }
        strcpy(new_node->word, word);
        new_node->next = NULL;

        // Hash the word to get the index in the table
        unsigned int index = hash(word);

        // Insert the new node into the hash table
        if (table[index] == NULL)
        {
            table[index] = new_node;
        }
        else
        {
            new_node->next = table[index];
            table[index] = new_node;
        }
    }

    // Close dictionary file
    fclose(file);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    unsigned int word_count = 0;
    for (int i = 0; i < HASH_TABLE_SIZE; i++)
    {
        node *cursor = table[i];
        while (cursor != NULL)
        {
            word_count++;
            cursor = cursor->next;
        }
    }
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < HASH_TABLE_SIZE; i++)
    {
        node *cursor = table[i];
        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
        table[i] = NULL;
    }
    return true;
}
