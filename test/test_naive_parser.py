import pytest
from main import PdfNumberParser

TEST_CASES = [
    ("samples/one_page_no_numbers.pdf", None),
    ("samples/100_chart_grid_(100).pdf", 100),
    ("samples/afwcf_body_text_(2025).pdf", 2025),
    ("samples/afwcf_line_chart_(2500).pdf", 2500),
    ("samples/afwcf_long_table_(4874).pdf", 4874),
    ("samples/afwcf_simple_table_(15873d5).pdf", 15873.5),
    ("samples/afwcf_table_no_lines_(8818d877).pdf", 8818.877),
    ("samples/afwcf_table_some_lines_(2025).pdf", 2025),
    ("samples/afwcf_title_page_(4930).pdf", 4930),
    ("samples/sample_invoice_(13201652).pdf", 13201652),
]

@pytest.mark.parametrize(
    "file,largest_number",
    TEST_CASES,
    ids=[case[0] for case in TEST_CASES],
)
def test_simple_number_extraction(file, largest_number):
    assert PdfNumberParser(file).find_largest_number() == largest_number