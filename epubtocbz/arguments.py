from argparse import ArgumentParser
from pathlib import Path

parser = ArgumentParser(description='''
Convert EPUB files to CBZ files
''')

parser.add_argument("from", type=Path, help='''
Where to find the EPUB files to convert. Can be a file or a directory for bulk conversion.
''')

parser.add_argument('-t', "--to", type=Path, help='''
Where to save the CBZ files to. Leave blank to save in from directory. 
Directory structure will be kept if doing bulk conversion.
''')

parser.add_argument('-o', "--overwrite", nargs="?", const=True, default=False, help='''
Enable overwriting of existing cbz files
''')

parser.add_argument("--spreads", dest="spreads", nargs="?", const=True, default=True, help='''
This will merge every pair of single pages into a spread, ignoring the cover, existing spreads and any last page.
On by default.
''')

parser.add_argument("--pages", dest="spreads", const=False, nargs="?", help='''
turns off spread merging.
''')

parser.add_argument("-rtl", "--manga", dest="manga", const=True,  nargs="?", default=None, help='''
Marks this book or books as having an RTL reading direction, and will merge spreads appropriately. 
By default the program will try and find this from the metadata
''')

parser.add_argument("-ltr", "--comics", dest="manga", const=False,  nargs="?", help='''
Marks this book or books as having an LTR reading direction, and will merge spreads appropriately.
By default the program will try and find this from the metadata
''')
