def main():
    card_number = input("Number: ")
    sum1 = 0
    sum2 = 0

    # Calculate the sum of the digits that weren’t multiplied by 2
    for digit in card_number[-1::-2]:
        sum1 += int(digit)

    # Multiply every other digit by 2, starting from the second-to-last digit
    for digit in card_number[-2::-2]:
        multiplied_digit = int(digit) * 2
        sum2 += multiplied_digit % 10 + multiplied_digit // 10

    # Calculate total sum
    total_sum = sum1 + sum2

    # Check if the total's last digit is 0
    if total_sum % 10 == 0:
        # Determine the type of card
        if (340000000000000 <= int(card_number) < 350000000000000) or \
           (370000000000000 <= int(card_number) < 380000000000000):
            print("AMEX")
        elif 5100000000000000 <= int(card_number) < 5600000000000000:
            print("MASTERCARD")
        elif (4000000000000 <= int(card_number) < 5000000000000) or \
             (4000000000000000 <= int(card_number) < 5000000000000000):
            print("VISA")
        else:
            print("INVALID")
    else:
        print("INVALID")


if __name__ == "__main__":
    main()
