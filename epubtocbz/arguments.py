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
This will attempt to analyse the pages in the epub and construct spreads based on the contents.
On by default.
''')

parser.add_argument("--pages", dest="spreads", const=False, nargs="?", help='''
turns off spread merging.
''')
