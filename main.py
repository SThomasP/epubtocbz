import gc

from images import open_image, create_spread

FORMAT = '{} {:003}.jpg'


def process_bulk_innards(fromzip, tozip, pages, book_name, progress, is_manga=True):
    page_count = len(pages)
    page = 0
    i = 0
    while i < page_count:
        page += 1
        if i == page_count - 1:
            tozip.writestr(FORMAT.format(book_name, page), fromzip.read(pages[i]))
            progress.update()
            i += 1
        else:
            image = open_image(fromzip, pages[i])
            iw, ih = image.size
            if iw > ih:
                tozip.writestr(FORMAT.format(book_name, page), fromzip.read(pages[i]))
                progress.update()
                i += 1
            else:
                if is_manga:
                    right = image
                    left = open_image(fromzip, pages[i + 1])
                else:
                    left = image
                    right = open_image(fromzip, pages[i + 1])
                spread = create_spread(right, left)
                tozip.writestr(FORMAT.format(book_name, page), spread)
                progress.update(2)
                i += 2
        gc.collect()