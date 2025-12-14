#!/usr/bin/env python3
"""
E-Reader HTML Fixer
Cleans up HTML book chapters for better e-reader compatibility
Removes external CSS/JS and adds readable inline styles
"""

import os
import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup


def extract_chapter_content(soup):
    """Extract the main chapter content from the HTML"""
    # Try to find the main content div
    content_div = soup.find('div', class_='txt')
    
    if not content_div:
        # Alternative: look for div with lots of paragraphs
        all_divs = soup.find_all('div')
        for div in all_divs:
            paragraphs = div.find_all('p')
            if len(paragraphs) > 10:  # Likely the main content
                content_div = div
                break
    
    return content_div


def get_chapter_title(soup):
    """Extract chapter title"""
    # Try multiple ways to find the title
    title_elem = soup.find('span', class_='chapter')
    if title_elem:
        return title_elem.get_text(strip=True)
    
    # Try h1 with class tit
    h1_elem = soup.find('h1', class_='tit')
    if h1_elem:
        return h1_elem.get_text(strip=True)
    
    # Fallback to page title
    title_tag = soup.find('title')
    if title_tag:
        return title_tag.get_text(strip=True)
    
    return "Chapter"


def clean_html_file(input_path, output_path):
    """Clean a single HTML file for e-reader compatibility"""
    
    print(f"Processing: {input_path}")
    
    # Read the original HTML
    with open(input_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Parse with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract title and content
    chapter_title = get_chapter_title(soup)
    content_div = extract_chapter_content(soup)
    
    if not content_div:
        print(f"  ⚠ Warning: Could not find main content in {input_path.name}")
        return False
    
    # Get all paragraphs
    paragraphs = content_div.find_all('p')
    
    # Remove any script tags or ad divs within paragraphs
    for p in paragraphs:
        for script in p.find_all('script'):
            script.decompose()
        for div in p.find_all('div'):
            div.decompose()
    
    # Create new clean HTML
    clean_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{chapter_title}</title>
    <style>
        body {{
            font-family: Georgia, serif;
            font-size: 1.2em;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #fafafa;
            color: #333;
        }}
        h1 {{
            font-size: 1.8em;
            margin-bottom: 0.5em;
            text-align: center;
            color: #222;
        }}
        p {{
            font-size: 1em;
            margin-bottom: 1em;
            text-align: justify;
        }}
    </style>
</head>
<body>
    <h1>{chapter_title}</h1>
"""
    
    # Add each paragraph
    for p in paragraphs:
        text = p.get_text(strip=True)
        if text:  # Only add non-empty paragraphs
            clean_html += f"    <p>{text}</p>\n"
    
    clean_html += """</body>
</html>"""
    
    # Write the cleaned HTML
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(clean_html)
    
    print(f"  ✓ Saved to: {output_path}")
    return True


def process_directory(input_dir, output_dir=None):
    """Process all HTML files in a directory"""
    
    input_path = Path(input_dir)
    
    if not input_path.exists():
        print(f"Error: Directory '{input_dir}' does not exist!")
        return
    
    # If no output directory specified, create one
    if output_dir is None:
        output_path = input_path.parent / f"{input_path.name}_cleaned"
    else:
        output_path = Path(output_dir)
    
    # Create output directory if it doesn't exist
    output_path.mkdir(exist_ok=True)
    
    # Find all HTML files
    html_files = list(input_path.glob("*.html")) + list(input_path.glob("*.htm"))
    
    if not html_files:
        print(f"No HTML files found in '{input_dir}'")
        return
    
    print(f"\nFound {len(html_files)} HTML file(s)")
    print(f"Output directory: {output_path}\n")
    
    # Process each file
    success_count = 0
    for html_file in sorted(html_files):
        output_file = output_path / html_file.name
        if clean_html_file(html_file, output_file):
            success_count += 1
    
    print(f"\n{'='*50}")
    print(f"Completed: {success_count}/{len(html_files)} files processed successfully")
    print(f"Cleaned files are in: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("E-Reader HTML Fixer")
        print("=" * 50)
        print("\nUsage:")
        print(f"  python {os.path.basename(__file__)} <input_directory> [output_directory]")
        print("\nExample:")
        print(f"  python {os.path.basename(__file__)} ./my_books")
        print(f"  python {os.path.basename(__file__)} ./my_books ./cleaned_books")
        print("\nThis will:")
        print("  ✓ Remove all external CSS and JavaScript")
        print("  ✓ Extract only the chapter text content")
        print("  ✓ Add clean, readable inline styles")
        print("  ✓ Make files compatible with your Ritmix reader")
        sys.exit(1)
    
    input_directory = sys.argv[1]
    output_directory = sys.argv[2] if len(sys.argv) > 2 else None
    
    process_directory(input_directory, output_directory)



