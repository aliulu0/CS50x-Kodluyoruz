#include <cs50.h>
#include <stdio.h>

int main(void)
{
    long credit_card;
    do
    {
        credit_card = get_long("Number: ");
    }
    while(credit_card < 0);

    long card_copy = credit_card;
    int sum = 0, count = 0;
    long divisor = 10;
    
    while(card_copy > 0)
    {
        int last_digit = card_copy % 10;
        sum = sum + last_digit;
        card_copy = card_copy /100;
    }
    card_copy = credit_card / 10 ;
    while(card_copy > 0)
    {
         int last_digit = card_copy % 10;
         int times_two = last_digit * 2;
         sum = sum + (times_two % 10) + (times_two / 10);
         card_copy = card_copy /100;
    }
    card_copy = credit_card;
    while(card_copy != 0 )
    {
        card_copy = card_copy / 10 ;
        count++;
    } 

    for(int i = 0; i < count - 2 ; i++)
    {
        divisor = divisor * 10;
    }

    int first_digit = credit_card / divisor;
    int first_two_digit = credit_card / (divisor/10);

    if(sum % 10 == 0)
    {
        // Visa numbers start with 4 and  uses 13- and 16-digit numbers
        // American Express numbers start with 34 or 37 and uses 15-digit numbers
        // MasterCard numbers start with 51, 52, 53, 54, or 55 and uses 16-digit numbers
        if(first_digit == 4 && (count ==13 || count == 16))
        {
            printf("VISA\n");
        }
        else if((first_two_digit == 34 || first_two_digit == 37) && count ==15)
        {
            printf("AMEX\n");
        }
        else if((first_two_digit > 50 && first_two_digit < 56) && count ==16)
        {
            printf("MASTERCARD\n");
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
}
