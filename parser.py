import pdfplumber
from collections import Counter, defaultdict
import re

def clean_text(text):
    """
    Clean garbled or duplicated text and normalize spacing.
    """
    # Collapse duplicated characters (e.g. "RReeqquueesstt" → "Request")
    text = re.sub(r'([A-Za-z])\1{1,}', r'\1', text)
    # Remove extra spaces
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()

def extract_pdf_data(pdf_path):
    """
    Extracts title and outline from any general PDF document.
    Returns JSON-compatible dictionary with 'title' and 'outline'.
    """
    title = ""
    outline = []

    with pdfplumber.open(pdf_path) as pdf:
        all_font_sizes = []
        all_chars = []

        for page in pdf.pages:
            chars = page.chars
            all_chars.extend([(char, page.page_number) for char in chars])
            all_font_sizes.extend([round(char["size"], 1) for char in chars])

        if not all_font_sizes:
            return {"title": "", "outline": []}

        # Most common font size → assumed body text size
        body_font_size = Counter(all_font_sizes).most_common(1)[0][0]

        # Group characters by line using Y-coordinate tolerance
        line_map = defaultdict(list)
        for char, page_num in all_chars:
            y = round(char["top"], 1)
            line_map[(page_num, y)].append(char)

        lines_by_page = defaultdict(list)

        for (page_num, y), chars in line_map.items():
            sorted_chars = sorted(chars, key=lambda c: c['x0'])
            line_text = ''.join(c['text'] for c in sorted_chars)
            font_sizes = [c['size'] for c in sorted_chars]
            avg_size = sum(font_sizes) / len(font_sizes)

            cleaned = clean_text(line_text)
            if len(cleaned.strip()) < 4:
                continue

            lines_by_page[page_num].append({
                "text": cleaned,
                "avg_size": avg_size,
                "page": page_num
            })

        # Define heading levels based on font size gaps
        unique_sizes = sorted(set(round(size, 1) for size in all_font_sizes), reverse=True)
        size_to_level = {}
        if unique_sizes:
            size_to_level[unique_sizes[0]] = "H1"
        if len(unique_sizes) > 1:
            size_to_level[unique_sizes[1]] = "H2"
        if len(unique_sizes) > 2:
            size_to_level[unique_sizes[2]] = "H3"
        if len(unique_sizes) > 3:
            size_to_level[unique_sizes[3]] = "H4"

        # Build outline from large-font lines
        seen = set()
        outline = []
        for page_num in sorted(lines_by_page.keys()):
            for entry in lines_by_page[page_num]:
                size = round(entry["avg_size"], 1)
                text = entry["text"]

                level = size_to_level.get(size)
                if not level:
                    continue  # Skip small or unknown sizes

                key = (text, page_num)
                if key in seen:
                    continue  # Skip duplicates
                seen.add(key)

                outline.append({
                    "level": level,
                    "text": text,
                    "page": page_num
                })

        # Title = first H1 on page 1, or fallback to first heading
        title = ""
        for h in outline:
            if h["level"] == "H1" and h["page"] == 1:
                title = h["text"]
                break
        if not title and outline:
            title = outline[0]["text"]

        return {
            "title": title,
            "outline": outline
        }
