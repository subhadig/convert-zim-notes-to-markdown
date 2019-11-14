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
        return line.replace(_bullet, "- ", 1)
    return line

def _parse_file(filename):
    output_filename = filename.split('.')[0] + '.markdown'

    reconversion = False
    if filename == output_filename:
        reconversion = True
        filename = filename + ".old" # Rename input file if it is markdown if reconverting to markdown
        os.rename(output_filename, filename)
    elif os.path.exists(output_filename):
        os.remove(output_filename) # Remove the output file if exists

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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', help='The path of the file')
    args = parser.parse_args()
    _parse_file(args.filepath)

if __name__=='__main__':
    main()
