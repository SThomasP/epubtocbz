from enum import Enum
from os import path
from .model import Position, ReadingDirection
from . import container, opf, xhtml


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
            images.append((img, item[1]))
    return images


def find_spreads(images, reading_direction):
    i = 0
    while i < len(images):
        position = images[i][1]
        if reading_direction == ReadingDirection.RTL:
            if position == Position.RIGHT and i < len(images) - 1:
                next_pos = images[i+1][1]
                if next_pos == Position.LEFT:
                    yield images[i+1][0], images[i][0]
                    i += 2
                else:
                    yield images[i][0]
                    i += 1
            else:
                yield images[i][0]
                i += 1
        elif reading_direction == ReadingDirection.LTR:
            if position == Position.LEFT and i < len(images) - 1:
                next_pos = images[i+1][1]
                if next_pos == Position.RIGHT:
                    yield images[i][0], images[i+1][0]
                    i += 2
                else:
                    yield images[i][0]
                    i += 1
            else:
                yield images[i][0]
                i += 1


def get_spreads_and_pages(epub_zip):
    opf_filename = container.get_opf_file_location(epub_zip)
    opf_file = opf.open_opf(epub_zip, opf_filename)
    reading_direction = opf.get_reading_direction(opf_file)
    spine_contents = opf.get_spine_contents(opf_file)
    images = get_images(spine_contents, opf_filename, epub_zip)
    return [spread for spread in find_spreads(images, reading_direction)]
