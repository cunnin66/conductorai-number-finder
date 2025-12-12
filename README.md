# conductorai-number-finder

> Take-home project for the ConductorAI Full-Stack Engineering Role

A PDF number extraction tool that finds the largest numerical value in a document using either a naive or context-aware advanced parser.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python3 ./main.py "path/to/file.pdf"
```

The file path can be an absolute path, relative path, or URL (quotes recommended).

### Options

| Flag | Description |
|------|-------------|
| `-v`, `--verbose` | Print the largest number found on each page |
| `-a`, `--advanced` | Use the advanced number parser (default: naive) |

---

## Naive Number Parser

**Goal:** Find the largest numerical value in the PDF, regardless of unit or magnitude qualifiers.

**Approach:**

1. Reading the PDF page by page, extract all identified text using pdfplumber.
2. Parse the extracted text using pattern recognition of known number formats (e.g., "-34", "4.2", "1,000,000")
3. Cast the numeric strings to integers/floats, and find the largest in the list

**Example:**

```
"1.2 million, which costs $1,025 a month for project 4E"
→ Extracts: [1.2, 1025, 4]
→ Returns: 1025
```

### Sample Results

Using the [FY25 Air Force Working Capital Fund](https://www.saffm.hq.af.mil/Portals/84/documents/FY25/FY25%20Air%20Force%20Working%20Capital%20Fund.pdf?ver=sHG_i4Lg0IGZBCHxgPY01g%3d%3d):

- **Largest value found:** 6,000,000 (page 93)

---

## Advanced Number Parser

**Goal:** Using local context to correct numerical magnitude, find the largest number in the document.

**Example:**

```
"1.2 million, which costs $1,025 a month for project 4E"
→ Extracts: [1,200,000, 1025]
→ Returns: 1,200,000
```

### Challenges Addressed

- Attaches magnitude indicators of various forms (`K`, `million`, `in billions`, scientific notation)
- Maps correct magnitude for grouped indicators (e.g., `"3.4 and 2.5, in millions"`)
- Differentiates numbers in names (`"Form 4E"`) from actual values (`"$4.2B in revenue"`)

### Sample Results

Using the [FY25 Air Force Working Capital Fund](https://www.saffm.hq.af.mil/Portals/84/documents/FY25/FY25%20Air%20Force%20Working%20Capital%20Fund.pdf?ver=sHG_i4Lg0IGZBCHxgPY01g%3d%3d):

- **Largest value found:** 9,600,000,000 (page 69)

---

## Known Limitations

- Designed to capture local qualifiers only; does not consider distant qualifiers such as those found in page or table headers
- Negative numbers represented in tables with parentheses (e.g., `(125.3)`) are erroneously interpreted as positive

## Future Work

Break each page into constituent components using pdfplumber's bounding box and table extraction features:

- Header
- Body text
- Table
- Chart
- Footer

**Planned improvements:**

1. **Tables:** Use table name, column headers, and row headers to determine magnitude of cell values
2. **Charts:** Use chart title and axis labels to determine magnitude of displayed values
3. **Page headers/footers:** Apply magnitude indicators to all numbers in body, tables, and charts if not otherwise qualified
4. **Multi-page tables:** Detect tables spanning multiple pages and apply header information from the first page to subsequent pages