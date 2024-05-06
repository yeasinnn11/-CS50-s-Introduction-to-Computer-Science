#include <cs50.h>
#include <stdio.h>

int main(void)
{
    long long card_number;
    int sum1 = 0, sum2 = 0, total_sum;

    // Prompt the user for a credit card number
    do
    {
        card_number = get_long("Number: ");
    }
    while (card_number <= 0);

    // Calculate the sum of the digits that weren’t multiplied by 2
    for (long long temp = card_number; temp > 0; temp /= 100)
    {
        sum1 += temp % 10;
    }

    // Multiply every other digit by 2, starting from the second-to-last digit
    for (long long temp = card_number / 10; temp > 0; temp /= 100)
    {
        int digit = (temp % 10) * 2;
        sum2 += digit % 10 + digit / 10;
    }

    // Calculate total sum
    total_sum = sum1 + sum2;

    // Check if the total's last digit is 0
    if (total_sum % 10 == 0)
    {
        // Determine the type of card
        if ((card_number >= 340000000000000 && card_number < 350000000000000) ||
            (card_number >= 370000000000000 && card_number < 380000000000000))
        {
            printf("AMEX\n");
        }
        else if (card_number >= 5100000000000000 && card_number < 5600000000000000)
        {
            printf("MASTERCARD\n");
        }
        else if ((card_number >= 4000000000000 && card_number < 5000000000000) ||
                 (card_number >= 4000000000000000 && card_number < 5000000000000000))
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }

    return 0;
}
