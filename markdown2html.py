#!/usr/bin/python3

"""
Markdown to HTML converter.

This script takes two arguments: the input Markdown file and the output HTML file.
It converts the Markdown content to HTML and writes it to the output file.

Usage: ./markdown2html.py README.md README.html
"""

import sys
import os

def markdown_to_html(markdown_file, html_file):
    """
    Convert Markdown content to HTML.

    Args:
        markdown_file (str): Input Markdown file
        html_file (str): Output HTML file

    Returns:
        None
    """
    with open(markdown_file, 'r') as f:
        markdown_content = f.read()

    html_content = ''
    lines = markdown_content.split('\n')
    for line in lines:
        if line.startswith('#'):
            heading_level = len(line) - len(line.lstrip('#'))
            html_content += f'<h{heading_level}>{line.strip("# ").strip()}</h{heading_level}>'
        elif line.startswith('- ') or line.startswith('* '):
            if not html_content.endswith('</ul>\n') and not html_content.endswith('</ol>\n'):
                html_content += '<ul>\n' if line.startswith('- ') else '<ol>\n'
            html_content += f'<li>{line.strip("- * ").strip()}</li>\n'
        else:
            if html_content.endswith('</ul>\n') or html_content.endswith('</ol>\n'):
                html_content = html_content.rstrip('</ul>\n</ol>\n') + '</ul>\n' if line.startswith('- ') else '</ol>\n'
            html_content += f'<p>{line.replace("\n", "<br/>\n")}</p>\n'

    with open(html_file, 'w') as f:
        f.write(html_content)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.stderr.write(f'Usage: {sys.argv[0]} README.md README.html\n')
        sys.exit(1)

    markdown_file = sys.argv[1]
    html_file = sys.argv[2]

    if not os.path.exists(markdown_file):
        sys.stderr.write(f'Missing {markdown_file}\n')
        sys.exit(1)

    markdown_to_html(markdown_file, html_file)
    sys.exit(0)
