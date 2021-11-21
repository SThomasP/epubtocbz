from argparse import ArgumentParser
from pathlib import Path

parser = ArgumentParser(description="Convert epub files to cbz files")

parser.add_argument("from", type=Path, help='''
Where to find the epubs to convert. Can be a file or a directory for bulk conversion.
''')

parser.add_argument('-t', "--to", type=Path, help='''
Where to save the cbz files to. Leave blank to save in from directory. 
Directory structure will be kept if doing bulk conversion.
''')

parser.add_argument("--spreads", dest="spreads", nargs="?", const=True, default=True, help='''
This will merge every pair of single pages into a spread, ignoring the cover and any last page.
on by default. Existing spreads will be skipped.
''')

parser.add_argument("--pages", dest="spreads", const=False, nargs="?", help='''
turns off spread merging
''')

parser.add_argument("-rtl", "--manga", dest="manga", const=True,  nargs="?", default=None, help='''
Marks this book or books as having an rtl reading direction, and will merge spreads appropriately. 
Leave blank to let the meta-data parser determine this (Program will fail if it can't)
''')

parser.add_argument("-ltr", "--comics", dest="manga", const=False,  nargs="?", help='''
Marks this book or books as having an ltr reading direction, and will merge spreads appropriately.
Leave blank to let the meta-data parser determine this (Program will fail if it can't)
''')
