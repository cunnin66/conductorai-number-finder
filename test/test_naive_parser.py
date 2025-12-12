import pytest
from main import PdfNumberParser

NAIVE_TEST_CASES = [
    ("samples/one_page_no_numbers.pdf", None),
    ("samples/100_chart_grid_(100).pdf", 100),
    ("samples/afwcf_body_text_n(2025)_a(1730800000).pdf", 2025),
    ("samples/afwcf_line_chart_(2500).pdf", 2500),
    ("samples/afwcf_long_table_(4874).pdf", 4874),
    ("samples/afwcf_simple_table_(15873d5).pdf", 15873.5),
    ("samples/afwcf_table_no_lines_n(10207d404)_a(10207404000).pdf", 10207.404),
    ("samples/afwcf_table_some_lines_(2025).pdf", 2025),
    ("samples/afwcf_title_page_(4930).pdf", 4930),
    ("samples/sample_invoice_(13201652).pdf", 13201652),
    ("samples/afwcf_page_56_n(5162d504)_a(5162504000).pdf", 5162.504),
    ("samples/afwcf_page_34_n(21941d905)_a(21941905000).pdf", 21941.905),
]

@pytest.mark.parametrize(
    "file,largest_number",
    NAIVE_TEST_CASES,
    ids=[case[0] for case in NAIVE_TEST_CASES],
)
def test_simple_number_extraction(file, largest_number):
    assert PdfNumberParser(file).find_largest_number() == largest_number