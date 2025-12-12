import io
import time
import argparse
import requests
import pdfplumber
from utils.num_extractor import extract_numbers


class PdfNumberParser:
    def __init__(self, file: str):
        self.file = file
        if file.startswith(("http://", "https://")):
            response = requests.get(file)
            response.raise_for_status()
            self.file = io.BytesIO(response.content)

    def find_largest_number(self):
        largest_number = None

        with pdfplumber.open(self.file) as pdf:
            for page in pdf.pages:
                text = page.extract_text()

                for number in extract_numbers(text):
                    if largest_number is None or number > largest_number:
                        largest_number = number

        return largest_number


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("file", type=str)
    args = arg_parser.parse_args()

    start_time = time.time()
    num_parser = PdfNumberParser(args.file)
    largest_number = num_parser.find_largest_number()
    end_time = time.time()

    print("*" * 100)
    print("Approach: Naive Parser")
    print(f"Time taken: {round(end_time - start_time, 3)} seconds")
    print(f"Largest number found: {largest_number}")
    print("*" * 100)