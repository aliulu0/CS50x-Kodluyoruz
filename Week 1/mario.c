#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while( height < 1 || height > 8);

    for(int row = 1; row <= height; row++)
    {
        /*
        
        ...# -> heihgt - row => 4 - 1 = 3 
        ..##  
        .### 
        #### 

        */
        for(int k = 1; k <= height - row; k++)
        {
            printf(" ");
        }
        for(int j = 1; j <= row; j++)
        {
            printf("#");
        }
          printf("\n");
    }
  

}

  
