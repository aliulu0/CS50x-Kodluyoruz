from cs50 import get_int

while True:
    credit = get_int("Number: ")
    if (credit > 0):
        break
card_copy = credit
total = 0
count = 0
divisor = 10

while (card_copy > 0):
    last_digit = card_copy % 10
    total += last_digit
    card_copy //= 100

card_copy = credit // 10
while (card_copy > 0):
    last_digit = card_copy % 10
    times_two = last_digit * 2
    total += (times_two % 10) + (times_two // 10)
    card_copy //= 100

card_copy = credit
while (card_copy != 0):
    card_copy = card_copy // 10
    count += 1

for i in range(count -2):
    divisor *= 10

first_digit = credit // divisor;
first_two_digit = credit // (divisor // 10);

if (total % 10 == 0):

# Visa numbers start with 4 and  uses 13- and 16-digit numbers
# American Express numbers start with 34 or 37 and uses 15-digit numbers
# MasterCard numbers start with 51, 52, 53, 54, or 55 and uses 16-digit numbers
    if (first_digit == 4 and (count == 13 or count == 16) ):
        print("VISA")

    elif ( (first_two_digit == 34 or first_two_digit == 37) and (count == 15) ):
        print("AMEX")

    elif ( (first_two_digit > 50 and first_two_digit < 56 ) and (count == 16) ):
        print("MASTERCARD")

    else:
         print("INVALID")

else:
    print("INVALID")