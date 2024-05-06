def main(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid Prompt")


height = main("Height: ")

while height < 1 or height > 8:
    print("height must be between 1 to 8")
    height = main("Height: ")

for i in range(1, height + 1):
    print(" " * (height - i) + "#" * i)
