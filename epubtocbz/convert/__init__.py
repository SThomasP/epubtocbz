import gc
from sys import stdout
from zipfile import ZipFile

from tqdm import tqdm
from epubtocbz.convert import internals, images

FORMAT = 'page_{:003}.jpg'


def process_epub(epub, cbz, make_spreads):
    book_name = epub.stem
    with ZipFile(epub, 'r') as epub_zip:
        pages = internals.get_spreads_and_pages(epub_zip, make_spreads)
        with ZipFile(cbz, "w") as cbz_zip:
            i = 1
            for page in tqdm(pages, desc=book_name):
                if type(page) is tuple:
                    img = images.create_spread(epub_zip.read(page[1]), epub_zip.read(page[0]))
                else:
                    img = epub_zip.read(page)
                write_image(cbz_zip, img, i)
                i += 1
    gc.collect()


def write_image(cbz_zip, image, number):
    cbz_zip.writestr(FORMAT.format(number), image)
