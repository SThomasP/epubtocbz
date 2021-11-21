import gc
from zipfile import ZipFile
from sys import stdout
from progress.bar import PixelBar

from convert import metadata, images

FORMAT = 'page_{:003}.jpg'


def get_pages(zipfile, metainfo):
    page_names = metadata.get_pages(metainfo)
    pages = [zipfile.getinfo(x) for x in page_names]
    return pages


def process_epub(epub, cbz):
    book_name = epub.stem
    with ZipFile(epub, 'r') as epub_zip:
        metainfo = metadata.get_meta_xml(epub_zip.read("content.opf").decode("utf-8"))
        pages = get_pages(epub_zip, metainfo)
        with ZipFile(cbz, "w") as cbz_zip:
            bar = PixelBar(book_name, max=len(pages), check_tty=False, file=stdout)
            write_image(cbz_zip, epub_zip.read(pages[0]), 0)
            bar.next()
            process_bulk_innards(epub_zip, cbz_zip, pages[1::], 1, bar, metadata.is_manga(metainfo))
            bar.finish()


def process_bulk_innards(epub_zip, cbz_zip, pages, start, progress, is_manga):
    page_count = len(pages)
    page = start - 1
    i = 0
    while i < page_count:
        page += 1
        if i == page_count - 1:
            write_image(cbz_zip, epub_zip.read(pages[i]), page)
            progress.next()
            i += 1
        else:
            image = images.open_image(epub_zip.read(pages[i]))
            iw, ih = image.size
            if iw > ih:
                write_image(cbz_zip, epub_zip.read(pages[i]), page)
                progress.next()
                i += 1
            else:
                if is_manga:
                    right = image
                    left = images.open_image(epub_zip.read(pages[i + 1]))
                else:
                    left = image
                    right = images.open_image(epub_zip.read(pages[i + 1]))
                spread = images.create_spread(right, left)
                write_image(cbz_zip, spread, page)
                progress.next(2)
                i += 2
        gc.collect()


def write_image(cbz_zip, image, number):
    cbz_zip.writestr(FORMAT.format(number), image)
