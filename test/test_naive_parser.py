import pytest
from utils.num_extractor import extract_numbers

@pytest.mark.parametrize(
    "pdf_text,expected",
    [
        pytest.param("There are no numbers here.", [], id="no_numbers"),
        pytest.param("This file has numbers 10, 20, and 5.", [10, 20, 5], id="comma_separated_numbers"),
        pytest.param("Maximum number is 999999 while others are 2 and 3.", [999999, 2, 3], id="multiple_numbers"),
    ],
)
def test_simple_number_extraction(pdf_text, expected):
    numbers = extract_numbers(pdf_text)
    assert set(numbers) == set(expected)