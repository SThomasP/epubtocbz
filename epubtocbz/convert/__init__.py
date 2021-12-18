import gc
from zipfile import ZipFile
from sys import stdout
from progress.bar import PixelBar

from epubtocbz.convert import metadata, images

FORMAT = 'page_{:003}.jpg'


class Bar(PixelBar):
    check_tty = False
    file = stdout
    # Braille pattern dots-0, means bar stays same width even if font isn't monospaced
    empty_fill = '⠀'


def get_pages(zipfile, opf_file):
    page_names = metadata.get_pages(opf_file)
    pages = [zipfile.getinfo(x) for x in page_names]
    return pages


def process_epub(epub, cbz, options):
    book_name = epub.stem
    with ZipFile(epub, 'r') as epub_zip:
        opf_file = metadata.get_meta_xml(epub_zip.read("content.opf").decode("utf-8"))
        pages = get_pages(epub_zip, opf_file)
        with ZipFile(cbz, "w") as cbz_zip:
            bar = Bar(book_name, max=len(pages))
            write_image(cbz_zip, epub_zip.read(pages[0]), 0)
            bar.next()
            if options['spreads']:
                generator = process_spreads(epub_zip, cbz_zip, pages[1::], 1, is_manga(options, opf_file))
            else:
                generator = process_singles(epub_zip, cbz_zip, pages[1::])
            for i in generator:
                bar.next(i)
            bar.finish()


def is_manga(options, opf_file):
    if options['manga'] is None:
        return metadata.is_manga(opf_file)
    return bool(options['manga'])


def process_singles(epub_zip, cbz_zip, pages):
    for i in range(len(pages)):
        write_image(cbz_zip, epub_zip.read(pages[i]), i + 1)
        yield 1


def process_spreads(epub_zip, cbz_zip, pages, start, manga):
    page_count = len(pages)
    page = start - 1
    i = 0
    while i < page_count:
        page += 1
        if i == page_count - 1:
            write_image(cbz_zip, epub_zip.read(pages[i]), page)
            up = 1
        else:
            image = images.open_image(epub_zip.read(pages[i]))
            iw, ih = image.size
            if iw > ih:
                write_image(cbz_zip, epub_zip.read(pages[i]), page)
                up = 1
            else:
                if manga:
                    right = image
                    left = images.open_image(epub_zip.read(pages[i + 1]))
                else:
                    left = image
                    right = images.open_image(epub_zip.read(pages[i + 1]))
                spread = images.create_spread(right, left)
                write_image(cbz_zip, spread, page)
                up = 2
        i += up
        yield up
        gc.collect()


def write_image(cbz_zip, image, number):
    cbz_zip.writestr(FORMAT.format(number), image)
