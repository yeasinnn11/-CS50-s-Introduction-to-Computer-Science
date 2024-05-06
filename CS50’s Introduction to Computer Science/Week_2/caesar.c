#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <stdlib.h>

// Function prototype
void encrypt(string plaintext, int key);

int main(int argc, string argv[])
{
    // Check if the user provided exactly one command-line argument
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // Check if the provided key consists of only digits
    for (int i = 0; argv[1][i] != '\0'; i++)
    {
        if (!isdigit(argv[1][i]))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }

    // Convert the key from string to an integer
    int key = atoi(argv[1]);

    // Prompt the user for plaintext
    string plaintext = get_string("plaintext: ");

    // Encrypt the plaintext using the given key
    encrypt(plaintext, key);

    printf("ciphertext: %s\n", plaintext);

    return 0;
}

// Function to encrypt plaintext using the Caesar cipher with a given key
void encrypt(string plaintext, int key)
{
    for (int i = 0; plaintext[i] != '\0'; i++)
    {
        if (isalpha(plaintext[i]))
        {
            // Determine whether the character is uppercase or lowercase
            char base = isupper(plaintext[i]) ? 'A' : 'a';
            // Apply the Caesar cipher encryption
            plaintext[i] = ((plaintext[i] - base + key) % 26) + base;
        }
    }
}
