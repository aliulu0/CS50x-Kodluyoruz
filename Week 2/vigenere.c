#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

bool check_valid_key(string s);
void encrypt(string plaintext,string ciphertext,string k);

int main(int argc, string argv[])
{
    if( argc != 2  || check_valid_key(argv[1]) == false )
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    
      string k = argv[1];
      string plaintext = get_string("plaintext: ");
      int n = strlen(plaintext);
      char ciphertext[n + 1 ];
      encrypt(plaintext,ciphertext,k);
      printf("ciphertext: %s\n",ciphertext);
      return 0;
   
}
void encrypt( string plaintext, string ciphertext, string k)
{   int i = 0;
    int j = 0;
    for(i = 0 ,j = 0; i<strlen(plaintext); i++)
    {
         j = j % strlen(k);
         char ch = plaintext[i];
         char c = k[j];         
         if(isalpha(ch))
         {
            //c(i) = (p(i) + k(j)) % 26
            // p(i) -> current character as int(a->0 b->1 c->2)
            // k(j) --> key
            char temp = tolower(ch);
            int pi = temp - 'a';
            char shift = tolower(c);
            int kj = shift - 'a';
            char ci = ((pi + kj) % 26) + 'a';
            if(islower(ch))
            {
                ciphertext[i] = ci;
            }
            else
            {
                ciphertext[i] = toupper(ci);
            }
            j++;
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
        if( isalpha(c) == false )
        {
            return false;
        }
    }
    return true;
}
