import pytest
from utils.num_extractor import extract_numbers, extract_numbers_with_magnitude

SIMPLE_TEST_CASES = [
    pytest.param("There are no numbers here.", [], id="no_numbers"),
    pytest.param("This file has numbers 10, 20, and 5.", [10, 20, 5], id="comma_separated_numbers"),
    pytest.param("Maximum number is 999999 while others are 2 and 3.", [999999, 2, 3], id="multiple_numbers"),
    pytest.param("How should we handle decimal numbers line 425.5?", [425.5], id="decimal_numbers"),
    pytest.param("Should we include numbers with commas like 1,000,000?", [1000000], id="comma_separated"),
    pytest.param("What about numbers as part of words or names like A4?", [4], id="numbers_in_name"),
    pytest.param("Let's check -234, +345, and **12 - numbers with prefixes", [-234, 345, 12], id="prefixes"),
    pytest.param("Now scientific notation like 1.23e4 or 1.43E5?", [1.23, 4, 1.43, 5], id="scientific_notation"),
]

@pytest.mark.parametrize(
    "pdf_text,expected",
    SIMPLE_TEST_CASES,
)
def test_simple_number_extraction(pdf_text, expected):
    numbers = extract_numbers(pdf_text)
    assert set(numbers) == set(expected)


MAGNITUDE_TEST_CASES = [
    pytest.param("There are no numbers here.", [], id="no_numbers"),
    pytest.param("This file has numbers 10, 20, and 5.", [10, 20, 5], id="comma_separated_numbers"),
    pytest.param("Maximum number is 999999 while others are 2 and 3.", [999999, 2, 3], id="multiple_numbers"),
    pytest.param("How should we handle decimal numbers line 425.5?", [425.5], id="decimal_numbers"),
    pytest.param("Should we include numbers with commas like 1,000,000?", [1000000], id="comma_separated"),
    pytest.param("What about numbers as part of words or names like A4?", [4], id="numbers_in_name"),
    pytest.param("Let's check -234, +345, and **12 - numbers with prefixes", [-234, 345, 12], id="prefixes"),
    # start divergent behavior
    pytest.param("Now scientific notation like 1.23e4 or 1.43E5", [12_300, 143_000], id="scientific_notation"),
    pytest.param("Scientific notation like 1.23e-4 or 1.43E+05", [0.000123, 143_000], id="scientific_with_signs"),
    pytest.param("Numbers with magnitudes like 1K, 200m, and 3.25b", [1000, 200_000_000, 3_250_000_000], id="magnitudes"),
    pytest.param("Magnitudes with spaces like 1 K and 5 MM", [1_000, 5_000_000], id="magnitudes_with_spaces"),
    pytest.param("Magnitudes with commas like 1, in thousands and 5, M", [1_000, 5_000_000], id="magnitudes_with_commas"),
    pytest.param("Magnitudes with parentheses like 1(thousand) and 5.2 (in millions)", [1_000, 5_200_000], id="magnitudes_with_parentheses"),
    pytest.param("Numbers with qualifiers like 1 million and 2.4 in billions", [1_000_000, 2_400_000_000], id="qualifiers"),
    pytest.param("group qualifiers, such as 2.4 and 3.5 (in millions)", [2_400_000, 3_500_000], id="group_qualifiers"),
    pytest.param("False qualifiers should not match: 2.4 markings, or 3.5mm", [2.4, 3.5], id="false_qualifiers"),
    pytest.param("False upline qualifer 1.2 in millions. Should not influence 2.5", [1_200_000, 2.5], id="false_upline_qualifiers"),
    pytest.param("False downline qualifiers should not match: 2.4. Where 3.5 in thousands should", [2.4, 3_500], id="false_downline_qualifiers"),
    pytest.param("Example profit of $9.2 billion", [9_200_000_000], id="with_currency"),
    # Identifier patterns - should NOT be treated as magnitudes
    pytest.param("Fund 9B is a name, not 9 billion", [9, 9_000_000_000], id="identifier_fund_9b"),
    pytest.param("Model 3T and Version 2K are identifiers", [3, 2], id="identifier_model_version"),
    # But these SHOULD still work as magnitudes
    pytest.param("Revenue of 9.5B and costs of 10B", [9_500_000_000, 10_000_000_000], id="valid_magnitude_with_decimal"),
    pytest.param("The company made 50M in profit", [50_000_000], id="valid_magnitude_multi_digit"),
]
@pytest.mark.parametrize(
    "pdf_text,expected",
    MAGNITUDE_TEST_CASES,
)
def test_number_extraction_with_magnitude(pdf_text, expected):
    numbers = extract_numbers_with_magnitude(pdf_text)
    assert set(numbers) == set(expected)