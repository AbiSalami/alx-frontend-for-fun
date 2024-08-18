#!/usr/bin/python3
"""Markdown to HTML"""

import sys
import os.path
import re
import hashlib

def process_line(line):
    # Bold syntax: **text**
    line = line.replace('**', '<b>', 1).replace('**', '</b>', 1)

    # Italic syntax: __text__
    line = line.replace('__', '<em>', 1).replace('__', '</em>', 1)

    # MD5 hash: [[text]]
    md5_matches = re.findall(r'\[\[.+?\]\]', line)
    if md5_matches:
        for match in md5_matches:
            text = match[2:-2]
            hashed = hashlib.md5(text.encode()).hexdigest()
            line = line.replace(match, hashed)

    # Remove 'C' or 'c': ((text))
    remove_c_matches = re.findall(r'\(\(.+?\)\)', line)
    if remove_c_matches:
        for match in remove_c_matches:
            text = ''.join(c for c in match[2:-2] if c.lower() != 'c')
            line = line.replace(match, text)

    return line

def convert_markdown_to_html(input_file, output_file):
    with open(input_file, 'r') as read, open(output_file, 'w') as html:
        unordered_start, ordered_start, paragraph = False, False, False

        for line in read:
            line = process_line(line)
            length = len(line)
            headings = line.lstrip('#')
            heading_num = length - len(headings)
            unordered = line.lstrip('-')
            unordered_num = length - len(unordered)
            ordered = line.lstrip('*')
            ordered_num = length - len(ordered)

            # Headings
            if 1 <= heading_num <= 6:
                line = '<h{}>{}</h{}>\n'.format(heading_num, headings.strip(), heading_num)

            # Unordered lists
            if unordered_num:
                if not unordered_start:
                    html.write('<ul>\n')
                    unordered_start = True
                line = '<li>{}</li>\n'.format(unordered.strip())
            if unordered_start and not unordered_num:
                html.write('</ul>\n')
                unordered_start = False

            # Ordered lists
            if ordered_num:
                if not ordered_start:
                    html.write('<ol>\n')
                    ordered_start = True
                line = '<li>{}</li>\n'.format(ordered.strip())
            if ordered_start and not ordered_num:
                html.write('</ol>\n')
                ordered_start = False

            # Paragraphs
            if not (heading_num or unordered_num or ordered_num):
                if not paragraph and length > 1:
                    html.write('<p>\n')
                    paragraph = True
                elif length > 1:
                    html.write('<br/>\n')
                elif paragraph:
                    html.write('</p>\n')
                    paragraph = False

            if length > 1:
                html.write(line)

        if unordered_start:
            html.write('</ul>\n')
        if ordered_start:
            html.write('</ol>\n')
        if paragraph:
            html.write('</p>\n')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: ./markdown2html.py README.md README.html', file=sys.stderr)
        exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(input_file):
        print(f'Missing {input_file}', file=sys.stderr)
        exit(1)

    convert_markdown_to_html(input_file, output_file)
    exit(0)

