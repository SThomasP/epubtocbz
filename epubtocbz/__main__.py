from epubtocbz.arguments import parser
from epubtocbz.files import get_epub_and_cbz


def run(args):
    for epub, cbz in get_epub_and_cbz(args['from'], args['to'], args['overwrite']):
        print(epub, cbz)


run(vars(parser.parse_args()))

