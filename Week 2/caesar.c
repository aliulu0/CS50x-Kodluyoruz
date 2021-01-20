#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

bool check_valid_key(string s);
void encrypt(string plaintext,string ciphertext,int k);

int main(int argc, string argv[])
{
    if( argc != 2  || check_valid_key(argv[1]) == false )
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    
      int k = atoi(argv[1]);
      string plaintext = get_string("plaintext: ");
      int n = strlen(plaintext);
      char ciphertext[n + 1 ];
      encrypt(plaintext,ciphertext,k);
      printf("ciphertext: %s\n",ciphertext);
      return 0;
   
}
void encrypt( string plaintext, string ciphertext, int k)
{   int i = 0;
    
    for(i = 0; i<strlen(plaintext); i++)
    {
         char ch = plaintext[i];
         if(isalpha(ch))
         {
            //c(i) = (p(i) + k) % 26
            // p(i) -> current character as int(a->0 b->1 c->2)
            // k --> key
            char temp = tolower(ch);
            int pi = temp - 'a';
            char ci = ((pi + k) % 26) + 'a';
            if(islower(ch))
            {
                ciphertext[i] = ci;
            }
            else
            {
                ciphertext[i] = toupper(ci);
            }
        }
        else
        {
            ciphertext[i] = ch;
        }
    }
    ciphertext[i] = '\0';
}

bool check_valid_key(string s)
{
    for(int i = 0 ; i< strlen(s); i++)
    {
        char c = s[i];
        if( isdigit(c) == false )
        {
            return false;
        }
    }
    return true;
}
