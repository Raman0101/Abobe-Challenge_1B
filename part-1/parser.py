import pdfplumber
from collections import Counter, defaultdict
import re

def clean_text(text):
    """
    Cleans garbled or duplicated text and normalizes spacing.
    """
    # Collapse repeating characters (e.g. "RReeqquueesstt" -> "Request")
    text = re.sub(r'([A-Za-z])\1{1,}', r'\1', text)
    # Normalize whitespaces
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()

def extract_pdf_data(pdf_path):
    """
    Extracts the title, outline, and full content from a PDF.
    Returns a dictionary with 'title', 'outline', and 'content'.
    """
    with pdfplumber.open(pdf_path) as pdf:
        all_chars = []
        all_font_sizes = []

        # Collect all characters and font sizes from all pages
        for page in pdf.pages:
            chars = page.chars
            all_chars.extend([(char, page.page_number) for char in chars])
            all_font_sizes.extend([round(char['size'], 1) for char in chars])

        if not all_chars or not all_font_sizes:
            return {"title": "", "outline": [], "content": ""}

        # Determine the body font size (most common)
        body_font_size = Counter(all_font_sizes).most_common(1)[0][0]

        # Group characters by lines (using Y coordinate per page)
        line_map = defaultdict(list)
        for char, page_num in all_chars:
            y_key = round(char['top'], 1)
            line_map[(page_num, y_key)].append(char)

        # Process lines and calculate average font sizes
        lines_by_page = defaultdict(list)
        for (page_num, y), chars in line_map.items():
            sorted_chars = sorted(chars, key=lambda c: c['x0'])
            line_text = ''.join(c['text'] for c in sorted_chars)
            font_sizes = [round(c['size'], 1) for c in sorted_chars]
            avg_size = round(sum(font_sizes) / len(font_sizes), 1)

            cleaned = clean_text(line_text)
            if len(cleaned) < 4:
                continue  # Skip noise or garbage lines

            lines_by_page[page_num].append({
                "text": cleaned,
                "avg_size": avg_size,
                "page": page_num
            })

        # Identify heading levels by font size (descending)
        unique_sizes = sorted(set(all_font_sizes), reverse=True)
        size_to_level = {}
        heading_levels = ["H1", "H2", "H3", "H4"]
        for i in range(min(len(unique_sizes), len(heading_levels))):
            size_to_level[unique_sizes[i]] = heading_levels[i]

        # Construct outline
        seen = set()
        outline = []
        for page_num in sorted(lines_by_page.keys()):
            for entry in lines_by_page[page_num]:
                size = entry["avg_size"]
                text = entry["text"]

                level = size_to_level.get(size)
                if not level:
                    continue

                key = (text.lower(), page_num)
                if key in seen:
                    continue
                seen.add(key)

                outline.append({
                    "level": level,
                    "text": text,
                    "page": page_num
                })

        # Determine title (first H1 on page 1, or fallback)
        title = ""
        for h in outline:
            if h["level"] == "H1" and h["page"] == 1:
                title = h["text"]
                break
        if not title and outline:
            title = outline[0]["text"]

        # Construct full content as plain text
        full_text_lines = []
        for page in sorted(lines_by_page.keys()):
            for line in lines_by_page[page]:
                full_text_lines.append(line["text"])
        full_text = "\n".join(full_text_lines)

        return {
            "title": title,
            "outline": outline,
            "content": full_text
        }
