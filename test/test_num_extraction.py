import pytest
from utils.num_extractor import extract_numbers

@pytest.mark.parametrize(
    "pdf_text,expected",
    [
        pytest.param("There are no numbers here.", [], id="no_numbers"),
        pytest.param("This file has numbers 10, 20, and 5.", [10, 20, 5], id="comma_separated_numbers"),
        pytest.param("Maximum number is 999999 while others are 2 and 3.", [999999, 2, 3], id="multiple_numbers"),
        pytest.param("How should we handle decimal numbers line 425.5?", [425.5], id="decimal_numbers"),
        pytest.param("Should we include numbers with commas like 1,000,000?", [1000000], id="comma_separated"),
        pytest.param("What about numbers as part of words or names like A4?", [4], id="numbers_in_name"),
        pytest.param("Let's check -234, +345, and **12 - numbers with prefixes", [-234, 345, 12], id="prefixes"),
        pytest.param("Now scientific notation like 1.23e4 or 1.43E5?", [1.23, 4, 1.43, 5], id="scientific_notation"),
    ],
)
def test_simple_number_extraction(pdf_text, expected):
    numbers = extract_numbers(pdf_text)
    assert set(numbers) == set(expected)