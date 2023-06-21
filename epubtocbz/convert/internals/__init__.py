from os import path

from . import container, opf, xhtml
from .model import Position, ReadingDirection


def get_images(spine_contents: tuple, opf_filename: str, epub_file):
    images = []
    for item in spine_contents:
        i = item[0]
        mediatype = i.attrib['media-type']
        img = None
        if mediatype.startswith('image/'):
            img = path.join(path.dirname(opf_filename), i.attrib['href'])
        elif mediatype == 'application/xhtml+xml':
            xhtml_path = path.join(path.dirname(opf_filename), i.attrib['href'])
            img = xhtml.get_image(xhtml_path, epub_file)
        if img is not None:
            img = path.normpath(img)
            images.append((img, item[1]))
    return images


def find_spreads(images, spread_function, can_spread):
    i = 0
    while i < len(images):
        if can_spread(images, i):
            yield spread_function(images, i)
            i += 2
        else:
            yield images[i][0]
            i += 1


def make_can_spread(current_position, next_position):
    def can_spread(images, i):
        return images[i][1] == current_position and i < len(images) - 1 and images[i + 1][1] == next_position

    return can_spread


def get_direction_functions(reading_direction):
    if reading_direction == ReadingDirection.RTL:
        def make_spread(images, i):
            return images[i + 1][0], images[i][0]

        can_spread = make_can_spread(Position.RIGHT, Position.LEFT)
    elif reading_direction == ReadingDirection.LTR:
        def make_spread(images, i):
            return images[i][0], images[i + 1][0]

        can_spread = make_can_spread(Position.LEFT, Position.RIGHT)
    else:
        def make_spread(images, i):
            pass

        def can_spread(images, i):
            return False
    return make_spread, can_spread


def get_spreads_and_pages(epub_zip, make_spreads):
    opf_filename = container.get_opf_file_location(epub_zip)
    opf_file = opf.open_opf(epub_zip, opf_filename)
    spine_contents = opf.get_spine_contents(opf_file)
    images = get_images(spine_contents, opf_filename, epub_zip)
    if make_spreads:
        spread_function, can_spread = get_direction_functions(opf.get_reading_direction(opf_file))
        return [spread for spread in find_spreads(images, spread_function, can_spread)]
    else:
        return [i[0] for i in images]
