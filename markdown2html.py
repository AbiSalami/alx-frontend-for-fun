#!/usr/bin/python3

"""
Markdown to HTML converter

This script takes two command-line arguments: the name of the Markdown file
and the output file name. It converts the Markdown content to HTML and
writes it to the output file.

Usage: ./markdown2html.py README.md README.html
"""

import sys
import os
import markdown

def convert_markdown_to_html(markdown_file, output_file):
    """
    Convert Markdown content to HTML and write it to the output file.

    Args:
        markdown_file (str): The name of the Markdown file.
        output_file (str): The name of the output file.

    Returns:
        None
    """
    if not os.path.exists(markdown_file):
        sys.stderr.write(f"Missing {markdown_file}\n")
        sys.exit(1)

    with open(markdown_file, 'r') as f:
        markdown_content = f.read()

    html_content = markdown.markdown(markdown_content)

    with open(output_file, 'w') as f:
        f.write(html_content)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)

    markdown_file = sys.argv[1]
    output_file = sys.argv[2]

    convert_markdown_to_html(markdown_file, output_file)
    sys.exit(0)
