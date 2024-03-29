#!/usr/bin/env python3

'''
This script converts a Zim wiki formatted text file to
markdown formatted file.

Invocation:
convert_notes.py <path_to_zim_wiki_file>

Output will be stored in the invocation location
'''

import argparse
import os

_h1 = "======"
_h2 = "====="
_h3 = "===="
_h4 = "==="
_h5 = "=="
_bold = "** "
_bullet = "* "

_allowed_input_file_extension = [".txt", ".markdown"]

def _convert_line(line):
    if line.startswith(_h1):
        return line.replace(_h1, "#", 1).replace(_h1, "")
    elif line.startswith(_h2):
        return line.replace(_h2, "##", 1).replace(_h2, "")
    elif line.startswith(_h3):
        return line.replace(_h3, "###", 1).replace(_h3, "")
    elif line.startswith(_h4):
        return line.replace(_h4, "####", 1).replace(_h4, "")
    elif line.startswith(_h5):
        return line.replace(_h5, "#####", 1).replace(_h5, "")
    elif line.startswith(_bold):
        return line.replace(_bold, "**", 1).replace(" **", "**", 1)
    elif line.startswith(_bullet):
        return line.replace(_bullet, "- ", 1) # Because I prefer "- " over "* " for unnumbered lists
    return line

def _is_file_allowed(filename):
    for each in _allowed_input_file_extension:
        if filename.endswith(each):
            return True
    return False

def _parse_file(filename, delete):
    if not _is_file_allowed(filename):
        return

    output_filename = filename.rsplit('.')[0] + '.markdown'

    reconversion = False
    if filename == output_filename:
        reconversion = True
        filename = filename + ".old" # Rename input file if it is markdown if reconverting to markdown
        os.rename(output_filename, filename)
    elif os.path.exists(output_filename):
        os.remove(output_filename) # Remove the output file if exists

    print("Converting: " + filename)

    # Read lines from input file, convert and write to output file
    line_number = -1
    with open(output_filename, 'w') as out_file:
        with open(filename, 'r') as in_file:
            for line in in_file:
                line_number += 1
                if not reconversion and line_number < 4:
                    continue
                line = _convert_line(line)
                out_file.write(line)

    if delete:
        os.remove(filename)

def _handle_dir(dirname, delete):
    result = os.walk(dirname)
    for root,_,files in result:
        for each in files:
            _parse_file(os.path.join(root,each), delete)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', help='The path of the file')
    parser.add_argument('--delete', help='Delete the old wiki files', action='store_true')
    args = parser.parse_args()

    if os.path.isdir(args.filepath):
        _handle_dir(args.filepath, args.delete)
    else:
        _parse_file(args.filepath, args.delete)

if __name__=='__main__':
    main()
