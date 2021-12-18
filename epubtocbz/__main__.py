from epubtocbz.arguments import parser
from epubtocbz.files import get_epub_and_cbz
from epubtocbz.convert import process_epub


def run(args):
    options = {
        'spreads': args['spreads'],
        'manga': args['manga']
    }
    for epub, cbz in get_epub_and_cbz(args['from'], args['to'], args['overwrite']):
        # CBZ directory might not exist
        cbz.parent.mkdir(parents=True, exist_ok=True)
        process_epub(epub, cbz, options)


run(vars(parser.parse_args()))

