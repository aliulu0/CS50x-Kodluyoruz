#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    float dollars;

    do
    {
        dollars = get_float("Change owed: ");
    }
    while(dollars<0);

    int cents = round(dollars * 100);
    int coins = 0;
    while(cents != 0)
    {
        //25
        coins += (cents / 25);
        cents = cents % 25;

        //10
        coins += (cents / 10);
        cents = cents % 10;

        //5
        coins += (cents / 5);
        cents = cents % 5;

        //1
        coins += (cents /1);
        cents = cents % 1;
    }
    printf("I have %i coin(s)\n",coins);

}
