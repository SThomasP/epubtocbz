import gc
from zipfile import ZipFile
from sys import stdout
from progress.bar import PixelBar

from epubtocbz.convert import internals, images

FORMAT = 'page_{:003}.jpg'


def process_epub(epub, cbz, options):
    book_name = epub.stem
    with ZipFile(epub, 'r') as epub_zip:
        pages = internals.get_spreads_and_pages(epub_zip)
        with ZipFile(cbz, "w") as cbz_zip:
            pixel_bar = PixelBar(book_name, check_tty=False, file=stdout, empty_fill='⠀')
            for page in pixel_bar.iter(pages):
                if type(page) is tuple:
                    img = images.create_spread(epub_zip.read(page[1]), epub_zip.read(page[0]))
                else:
                    img = epub_zip.read(page)
                write_image(cbz_zip, img, pixel_bar.index)
    gc.collect()


def write_image(cbz_zip, image, number):
    cbz_zip.writestr(FORMAT.format(number), image)
