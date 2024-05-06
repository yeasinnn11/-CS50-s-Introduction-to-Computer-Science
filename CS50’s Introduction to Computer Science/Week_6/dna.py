import csv
import sys


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)
    for i in range(sequence_length):
        count = 0
        while True:
            start = i + count * subsequence_length
            end = start + subsequence_length
            if sequence[start:end] == subsequence:
                count += 1
            else:
                break
        longest_run = max(longest_run, count)
    return longest_run


def main():
    # Check for correct usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py database.csv sequence.txt")
        sys.exit(1)

    # Read the CSV file
    csv_file = sys.argv[1]
    with open(csv_file) as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames
        individuals = list(reader)

    # Read the DNA sequence file
    dna_file = sys.argv[2]
    with open(dna_file) as file:
        dna_sequence = file.read()

    # Compute the longest run of consecutive repeats for each STR
    str_counts = {}
    for header in headers[1:]:
        str_counts[header] = longest_match(dna_sequence, header)

    # Compare the STR counts with the individuals in the CSV file
    for individual in individuals:
        match = True
        for header in headers[1:]:
            if int(individual[header]) != str_counts[header]:
                match = False
                break
        if match:
            print(individual['name'])
            return

    # If no match found
    print("No match")


if __name__ == "__main__":
    main()
