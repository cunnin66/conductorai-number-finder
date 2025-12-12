import pytest
from main import PdfNumberParser


ADVANCED_TEST_CASES = [
    ("samples/one_page_no_numbers.pdf", None),
    ("samples/100_chart_grid_(100).pdf", 100),
    ("samples/afwcf_body_text_n(2025)_a(1730800000).pdf", 1_730_800_000),
    ("samples/afwcf_long_table_(4874).pdf", 4874), # still fails to map distant qualifiers
    ("samples/afwcf_table_no_lines_n(10207d404)_a(10207404000).pdf", 10207.404), # still fails to map distant qualifiers
    ("samples/afwcf_page_56_n(5162d504)_a(5162504000).pdf", 5162.504), # still fails to map distant qualifiers
        ("samples/afwcf_page_34_n(21941d905)_a(21941905000).pdf", 21941.905), # still fails to map distant qualifiers
]
@pytest.mark.parametrize(
    "file,largest_number",
    ADVANCED_TEST_CASES,
    ids=[case[0] for case in ADVANCED_TEST_CASES],
)
def test_advanced_number_extraction(file, largest_number):
    assert PdfNumberParser(file).find_largest_number_advanced() == largest_number