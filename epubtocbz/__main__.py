from epubtocbz.arguments import parser
from epubtocbz.convert import process_epub
from epubtocbz.files import get_epub_and_cbz


def run(args):
    for epub, cbz in get_epub_and_cbz(args['from'], args['to'], args['overwrite']):
        # CBZ directory might not exist
        cbz.parent.mkdir(parents=True, exist_ok=True)
        process_epub(epub, cbz, args['spreads'])


run(vars(parser.parse_args()))
