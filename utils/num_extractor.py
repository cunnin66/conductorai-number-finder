import re

def extract_numbers(text: str) -> list[int | float]:
    # Match negative numbers, decimals, and comma-formatted numbers
    pattern = r'-?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?'
    matches = re.findall(pattern, text)
    
    results = []
    for num in matches:
        # Remove commas for parsing
        clean_num = num.replace(',', '')
        # Use float if decimal point present, otherwise int
        if '.' in clean_num:
            results.append(float(clean_num))
        else:
            results.append(int(clean_num))
    return results


UNIT_MAGNITUDES = {
    # Thousands
    "k": 10**3,
    "thousand": 10**3, # inclusive of plural "thousand"
    "in thousand": 10**3, # inclusive of plural "thousands"
    # Millions
    "m": 10**6,
    "million": 10**6,
    "in million": 10**6, # inclusive of plural "millions"
    # Billions
    "b": 10**9,
    "billion": 10**9,
    "in billion": 10**9, # inclusive of plural "billions"
    # Other
    "t": 10**12,
    "trillion": 10**12,
    "in trillion": 10**12, # inclusive of plural "trillions"
}

def extract_numbers_with_magnitude(text: str) -> list[int | float]:
    """
    Extract numbers from text, taking into account magnitude indicators.
    
    Handles:
    - Scientific notation (1.23e4, 1.43E-5)
    - Single-letter magnitudes (1K, 200M, 3.25B, 1T)
    - MM abbreviation for millions (5 MM)
    - Word magnitudes (million, billion, thousand, trillion)
    - "in X" qualifiers (in millions, in billions)
    - Parenthetical magnitudes (5.2 (in millions))
    - Distant qualifiers ((in millions) applying to preceding numbers)
    """
    results = []
    
    def parse_num(s: str) -> int | float:
        """Parse a number string, handling commas."""
        clean = s.replace(',', '')
        return float(clean) if '.' in clean else int(clean)
    
    def normalize(num: float) -> int | float:
        """Convert to int if it's a whole number."""
        return int(num) if isinstance(num, float) and num == int(num) else num
    
    # Number pattern (handles negative, commas, and decimals)
    num_pattern = r'-?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?'
    
    # Track consumed character positions to avoid double-counting
    consumed = [False] * len(text)
    
    def mark(start: int, end: int):
        for i in range(start, end):
            consumed[i] = True
    
    def is_free(start: int, end: int) -> bool:
        return not any(consumed[start:end])
    
    # 1. Scientific notation: 1.23e4, 1.43E-5, 1.43E+05
    # Reject if preceded or followed by letters - catches OCR artifacts like "Person1.n5e9l4"
    for m in re.finditer(rf'({num_pattern})[eE]([+-]?\d+)', text):
        if not is_free(m.start(), m.end()):
            continue
        # Check if preceded by a letter (OCR artifact)
        if m.start() > 0 and text[m.start() - 1].isalpha():
            continue
        # Check if followed by a letter (OCR artifact)
        if m.end() < len(text) and text[m.end()].isalpha():
            continue
        base = parse_num(m.group(1))
        exp = int(m.group(2))
        results.append(normalize(base * (10 ** exp)))
        mark(m.start(), m.end())
    
    # 2. Single-letter magnitudes - with safeguards against identifier patterns like "Fund 9B"
    # 
    # Strategy: Check if preceded by capitalized word + space (identifier pattern)
    # This catches: "Fund 9B", "Model 3T", "Version 2K" etc.
    
    def is_identifier_pattern(match_start: int) -> bool:
        """Check if preceded by a capitalized word + space (e.g., 'Fund 9B')."""
        # Look at up to 20 chars before the match
        prefix = text[max(0, match_start - 20):match_start]
        # Check for pattern: capitalized word followed by space(s) at the end
        return bool(re.search(r'[A-Z][a-z]*\s+$', prefix))
    
    # Single-letter magnitudes (attached or with space/comma, not followed by letters)
    # Handles: 1K, 200m, 3.25b, 1T, 1 K, 5 M, 5, M but NOT 3.5mm (millimeters) or "Fund 9B"
    # Note: Use [ \t]* instead of \s* to avoid matching across newlines (e.g., "10.5\nb" shouldn't match)
    # Also reject if followed by ), digits, or . - catches list items, OCR artifacts, and section numbers like "3.3 T."
    for m in re.finditer(rf'({num_pattern})[ \t]*[,]?[ \t]*([kKmMbBtT])(?![a-zA-Z\)0-9.])', text):
        if not is_free(m.start(), m.end()):
            continue
        if is_identifier_pattern(m.start()):
            continue  # Skip identifier patterns like "Fund 9B"
        # Check if preceded by a letter - this catches OCR artifacts like "M4a.i4n7t9enance"
        # where "7t" would incorrectly match as 7 trillion
        if m.start() > 0 and text[m.start() - 1].isalpha():
            continue
        num = parse_num(m.group(1))
        mag = UNIT_MAGNITUDES[m.group(2).lower()]
        results.append(normalize(num * mag))
        mark(m.start(), m.end())
    
    # 3. MM abbreviation for millions (requires preceding space to distinguish from mm/millimeters)
    for m in re.finditer(rf'({num_pattern})\s+([Mm][Mm])(?![a-zA-Z])', text):
        if not is_free(m.start(), m.end()):
            continue
        num = parse_num(m.group(1))
        results.append(normalize(num * 10**6))
        mark(m.start(), m.end())
    
    # 4. Word magnitudes with optional punctuation and parentheses
    word_mags = ['in trillion', 'in billion', 'in million', 'in thousand',
                 'trillion', 'billion', 'million', 'thousand']
    word_mag_pattern = '|'.join(re.escape(w) for w in word_mags)
    
    pattern = rf'({num_pattern})\s*[,]?\s*\(?\s*({word_mag_pattern})s?\)?(?=\s|$|[,.])'
    for m in re.finditer(pattern, text, re.IGNORECASE):
        if not is_free(m.start(), m.end()):
            continue
        num = parse_num(m.group(1))
        mag_key = m.group(2).lower()
        mag = UNIT_MAGNITUDES[mag_key]
        results.append(normalize(num * mag))
        mark(m.start(), m.end())
    
    # 5. Group qualifiers - parenthetical magnitudes that apply to numbers in the same group
    # A "group" is defined by sentence/line boundaries (newlines, periods, etc.)
    # This prevents a qualifier in one section from affecting numbers in unrelated sections
    
    def find_group_start(pos: int) -> int:
        """Find the start of the current group by looking backwards for boundaries."""
        # Look for newlines, sentence endings, or start of text
        search_text = text[:pos]
        # Find the last occurrence of group boundaries
        boundaries = [
            search_text.rfind('\n'),
            search_text.rfind('. '),
            search_text.rfind('.\t'),
            search_text.rfind('? '),
            search_text.rfind('! '),
        ]
        last_boundary = max(boundaries)
        return last_boundary + 1 if last_boundary >= 0 else 0
    
    for qual_match in re.finditer(rf'\(\s*({word_mag_pattern})s?\s*\)', text, re.IGNORECASE):
        mag_key = qual_match.group(1).lower()
        mag = UNIT_MAGNITUDES[mag_key]
        qual_start = qual_match.start()
        
        # Find the start of this group (sentence/line boundary)
        group_start = find_group_start(qual_start)
        group_text = text[group_start:qual_start]
        
        # Apply only to unconsumed numbers within this group
        for num_match in re.finditer(num_pattern, group_text):
            abs_start = group_start + num_match.start()
            abs_end = group_start + num_match.end()
            if not is_free(abs_start, abs_end):
                continue
            num = parse_num(num_match.group())
            results.append(normalize(num * mag))
            mark(abs_start, abs_end)
    
    # 6. Remaining plain numbers
    for m in re.finditer(num_pattern, text):
        if not is_free(m.start(), m.end()):
            continue
        results.append(parse_num(m.group()))
    
    return results