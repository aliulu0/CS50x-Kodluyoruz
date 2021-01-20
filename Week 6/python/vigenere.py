from cs50 import get_string
from sys import argv

if len(argv) != 2 or argv[1].isalpha() == False:
    print("Usage: python vigenere.py k")
    exit(1)

else:
    k = argv[1].lower()
    s = get_string("plaintext: ")
    j = 0
    print("ciphertext: ",end="")

    for i in s:
        if i.isalpha():

            ki = ord(k[j % len(k)]) - 97

            lower = i.lower()

            pi = ord(lower) - 97

            ci = ( ( (pi + ki) % 26) + 97)

            if i.isupper():
                c = chr(ci).upper()
            else:
                c = chr(ci)

            j += 1
        else:
            c = i

        print(c, end="")
        
print("")
exit(0)
