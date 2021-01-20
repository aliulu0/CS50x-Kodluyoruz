from cs50 import get_string
from sys import argv

if ( (len(argv) != 2) and (arg[1].isdigit() == False) ):
    print("Usage: python caesar.py k")

else:
    k = int(argv[1])
    s = get_string("plaintext: ")
    print("ciphertext: ",end="")

    for i in s:
        if i.isalpha():

            lower = i.lower()

            pi = ord(lower) - 97

            ci = ( ( (pi + k) % 26) + 97)

            if i.isupper():
                c = chr(ci).upper()
            else:
                c = chr(ci)

        else:
            c = i


        print(c, end="")


print("")
