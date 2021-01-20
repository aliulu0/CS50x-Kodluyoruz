#include <cs50.h>
#include <stdio.h>

int main(void)
{
    long card,card_copy;
    int sum = 0, position = 0, digit_len = 0;
    do
    {

        card = get_long("Numbers: ");
        card_copy = card;

        while(card < 0)
        {
            if( position % 2 != 0)
            {
                int temp = 2 * (card % 10);
                if(temp > 9)
                {
                    sum += (temp % 10 + temp / 10);//12 -> 12 % 10 = 2 and 12/10 = 1 => 2+1 = 3;
                }
                else
                {
                    sum += temp;
                }
            }
            else
            {
                sum += (card % 10);
            }
            card = card /10;
            position++;
            digit_len++;
          
        }

    }
    while(card < 0);
    // last digit
    if(sum % 10 == 0)
    {
        // American Express numbers start with 34 or 37 and uses 15-digit numbers
        // MasterCard numbers start with 51, 52, 53, 54, or 55 and uses 16-digit numbers
        // Visa numbers start with 4 and  uses 13- and 16-digit numbers
        long amex_start = card_copy/10000000000000;
        if((amex_start == 34|| amex_start== 37) && (digit_len == 15))
        {
            printf("AMEX\n");
            return 0;
        }

        long master_start = card_copy/100000000000000;
        if((master_start >= 51 && master_start <= 55) && (digit_len == 16))
        {
            printf("MASTERCARD\n");
            return 0;
        }

        long visa_start = card_copy/1000000000000;
        if( (visa_start == 4 || master_start / 10 == 4) && (digit_len == 13 || digit_len == 16))
        {
            printf("VISA\n");
            return 0;
            
        }
        printf("INVALID\n");

    }
    else
    {
        printf("INVALID\n");
        return 1;
        
    }
}
