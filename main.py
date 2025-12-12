import io
import time
import argparse
import requests
import pdfplumber
from utils.num_extractor import extract_numbers


class PdfNumberParser:
    def __init__(self, file: str, verbose: bool = False):
        self.file = file
        self.verbose = verbose

        if file.startswith(("http://", "https://")):
            response = requests.get(file)
            response.raise_for_status()
            self.file = io.BytesIO(response.content)

    def find_largest_number(self):
        overall_largest = None

        with pdfplumber.open(self.file) as pdf:
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                
                page_largest = None
                for number in extract_numbers(text):
                    if page_largest is None or number > page_largest:
                        page_largest = number
                
                if page_largest and (overall_largest is None or page_largest > overall_largest):
                    overall_largest = page_largest
                
                if self.verbose:
                    print(f"(DEBUG) Largest number on Page #{page_num + 1}: {page_largest if page_largest else '[None]'}")

        return overall_largest


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("file", type=str)
    arg_parser.add_argument("-v", "--verbose", action="store_true")
    args = arg_parser.parse_args()

    start_time = time.time()
    num_parser = PdfNumberParser(args.file, args.verbose)
    largest_number = num_parser.find_largest_number()
    end_time = time.time()

    print("*" * 100)
    print("Approach: Naive Parser")
    print(f"Time taken: {round(end_time - start_time, 3)} seconds")
    print(f"Largest number found: {largest_number}")
    print("*" * 100)