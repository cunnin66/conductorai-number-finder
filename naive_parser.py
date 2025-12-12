import time
import argparse
import pdfplumber
from utils.num_extractor import extract_numbers


def naive_parse(file: str):
    largest_number = None
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()

            for number in extract_numbers(text):
                if largest_number is None or number > largest_number:
                    largest_number = number
    return largest_number


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str)
    args = parser.parse_args()

    start_time = time.time()
    num = naive_parse(args.file)
    end_time = time.time()

    print("*" * 100)
    print("Approach: Naive Parser")
    print(f"Time taken: {end_time - start_time} seconds")
    print(f"Largest number found: {num}")
    print("*" * 100)