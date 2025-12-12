import pytest
from main import PdfNumberParser


ADVANCED_TEST_CASES = [
    ("samples/one_page_no_numbers.pdf", None),
    ("samples/100_chart_grid_(100).pdf", 100),
    ("samples/afwcf_body_text_n(2025)_a(1730800000).pdf", 1_730_800_000),
]
@pytest.mark.parametrize(
    "file,largest_number",
    ADVANCED_TEST_CASES,
    ids=[case[0] for case in ADVANCED_TEST_CASES],
)
def test_advanced_number_extraction(file, largest_number):
    assert PdfNumberParser(file).find_largest_number_advanced() == largest_number