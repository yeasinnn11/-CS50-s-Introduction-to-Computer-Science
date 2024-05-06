#include <cs50.h>
#include <stdio.h>

int main(void)
{
    string x = get_string("What's your name? ");
    printf("Hello, %s\n", x);
}
