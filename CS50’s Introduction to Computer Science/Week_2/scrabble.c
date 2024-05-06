
#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

// Function to calculate the score of a word
int calculateScore(string word)
{
    int points[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
    int score = 0;

    for (int i = 0, n = strlen(word); i < n; i++)
    {
        char ch = toupper(word[i]);
        if (ch >= 'A' && ch <= 'Z')
        {
            score += points[ch - 'A'];
        }
    }

    return score;
}

int main(void)
{
    // Prompt the user for two words
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Compute the score of each word
    int score1 = calculateScore(word1);
    int score2 = calculateScore(word2);

    // Print the winner
    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score1 < score2)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }

    return 0;
}
