#!/usr/bin/env python3

'''Kindle to Zim

A script to import your Kindle clippings to Zim Desktop Wiki.
    
Usage: kindle_to_zim.py My\ Clippings.txt

Author: Bruno C. Vellutini - https://brunovellutini.com
'''

import os
import argparse
import re
from datetime import datetime, timezone

def sanitize_file_name(file_name):
    # Remove <i> and <b> tags
    file_name = re.sub(r'<i>|</i>|<b>|</b>', '', file_name)

    # Replace spaces and special characters with underscores or hyphens
    file_name = re.sub(r'[^\w\s-]', '', file_name).strip().replace(' ', '_')
    file_name = re.sub(r'[-\s]+', '-', file_name)

    return file_name

def extract_book_title_author_name(line):
    # Extract the book title and author name from the first line of the entry
    match = re.match(r'^(?P<book_title>.+?)(\s\((?P<author_last_name>.+),\s(?P<author_first_name>.+)\))?$', line)
    if match:
        book_title = match.group('book_title')
        author_last_name = match.group('author_last_name')
        author_first_name = match.group('author_first_name')
        if author_last_name and author_first_name:
            author_name = '{} {}'.format(author_first_name, author_last_name)
        else:
            author_name = None
        return {'book_title': book_title, 'author_name': author_name}
    else:
        return None

def extract_entry_info(entry):
    # Extract the entry type (Note or Highlight), page, location, and date from the entry
    entry_type_match = re.match(r'^- Your (?P<entry_type>Note|Highlight|Bookmark)', entry)
    entry_page_match = re.match(r'.*page (?P<entry_page>\d+)(-\d+)?', entry)
    entry_location_match = re.match(r'.*Location (?P<entry_location>\d+(?:-\d+)?)', entry)
    entry_date_match = re.match(r'.*Added on (?P<entry_date>.+)$', entry)

    entry_type = entry_type_match.group('entry_type') if entry_type_match else None
    entry_page = entry_page_match.group('entry_page') if entry_page_match else None
    entry_location = entry_location_match.group('entry_location') if entry_location_match else None
    entry_date = entry_date_match.group('entry_date') if entry_date_match else None

    entry_info = {'entry_type': entry_type, 'entry_page': entry_page, 'entry_location': entry_location, 'entry_date': entry_date}
    return entry_info

def parse_kindle_clippings(file_name):
    # Read the file and split it into entries using the separator "=========="
    with open(file_name, 'r', encoding='utf-8-sig') as f:
        entries = f.read().split('==========\n')

    # Group the entries by book title
    books = {}
    for entry in entries:
        lines = entry.strip().split('\n')
        if len(lines) == 1:
            continue
        book_info = extract_book_title_author_name(lines[0].strip())
        entry_info = extract_entry_info(lines[1].strip())
        if len(lines) > 3:
            entry_text = lines[3].strip()
            entry_info['entry_text'] = entry_text
        else:
            entry_info['entry_text'] = None
        if book_info:
            book_title = book_info['book_title']
            author_name = book_info['author_name']
            if book_title not in books:
                books[book_title] = {'author_name': author_name, 'entries': []}
            books[book_title]['entries'].append(entry_info)
    return books

def export_kindle_clippings(books):
    total_books = len(books.keys())
    total_entries = 0
    # Export individual entries for each book to separate plain text files
    for book_title, book_info in books.items():
        out_name = sanitize_file_name(book_title) + '.txt'
        with open(out_name, 'w', encoding='utf-8') as f:
            # Write the Zim header with version 0.6 and creation date with timestamp
            f.write('Content-Type: text/x-zim-wiki\nWiki-Format: zim 0.6\nCreation-Date: {}\n\n'.format(datetime.now(timezone.utc).astimezone().replace(microsecond=0).isoformat()))

            # Write the book title as the title of the page
            f.write('====== {} ======\n'.format(book_title))
            
            # Write the date formatted differently
            f.write('Created {}\n\n'.format(datetime.now().strftime('%A %d %B %Y')))

            # Write the author name if it exists
            if book_info['author_name']:
                f.write('Author: {}\n\n'.format(book_info['author_name']))
                
            # Count entries
            entries = book_info['entries']
            total_entries += len(entries)

            # Write the entries
            for entry in entries:
                f.write('**Entry:** {}'.format(entry['entry_type']))
                if entry['entry_page']:
                    f.write(' / Page {}'.format(entry['entry_page']))
                if entry['entry_location']:
                    f.write(' / Location {}'.format(entry['entry_location']))
                f.write(' / {}\n'.format(entry['entry_date']))
                if entry['entry_text']:
                    f.write('**Text:** {}\n\n'.format(entry['entry_text']))

    # Print totals
    print('{} books, {} entries'.format(total_books, total_entries))

if __name__ == '__main__':
    # Parse the command-line arguments
    parser = argparse.ArgumentParser(description='Parse Kindle clippings and export individual entries for each book to separate plain text files')
    parser.add_argument('file_name', help='the name of the file to be processed')
    args = parser.parse_args()

    # Call the parse_kindle_clippings function with the file name argument
    books = parse_kindle_clippings(args.file_name)
    export_kindle_clippings(books)
