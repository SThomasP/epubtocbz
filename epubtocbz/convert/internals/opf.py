from xml.etree import ElementTree
from .model import ReadingDirection, Position

OPF_NS = {
    "opf": "http://www.idpf.org/2007/opf"
}


def open_opf(epub_zip, opf_filename):
    return ElementTree.fromstring(epub_zip.read(opf_filename).decode('utf-8'))


def get_position(p):
    if p == "page-spread-left":
        return Position.LEFT
    elif p == "page-spread-right":
        return Position.RIGHT
    return Position.UNKNOWN


def get_spine_contents(opf_file):
    items = []
    for item in opf_file.findall('./opf:spine/opf:itemref', OPF_NS):
        itemid = item.attrib['idref']
        position = get_position(item.attrib.get('properties'))
        i = opf_file.find("./opf:manifest/opf:item[@id='" + itemid + "']", OPF_NS)
        items.append((i, position))
    return items


def get_reading_direction(opf_file):
    spine = opf_file.find("./opf:spine", OPF_NS)
    if spine is not None and 'page-progression-direction' in spine.attrib:
        ppd = spine.attrib['page-progression-direction']
        if ppd == "rtl":
            return ReadingDirection.RTL
        elif ppd == "ltr":
            return ReadingDirection.LTR
    if is_manga_amazon(opf_file):
        return ReadingDirection.RTL
    return ReadingDirection.LTR


def is_manga_amazon(meta_xml):
    reading_direction = meta_xml.find("./opf:metadata/opf:meta[@name='primary-writing-mode']", OPF_NS)
    if reading_direction is not None:
        if reading_direction.attrib['content'].endswith("rl"):
            return ReadingDirection.RTL
        return ReadingDirection.LTR
    return ReadingDirection.UNKNOWN
