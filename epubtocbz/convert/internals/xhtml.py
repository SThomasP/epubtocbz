from os import path
from xml.etree import ElementTree

XHTML_NS = {
    'xhtml': 'http://www.w3.org/1999/xhtml',
    'svg': 'http://www.w3.org/2000/svg',
    'xlink': 'http://www.w3.org/1999/xlink'
}


def get_tree(xhtml_path, epub_file):
    return ElementTree.fromstring(epub_file.read(xhtml_path).decode('utf-8'))


def find_img(tree):
    img = tree.find('.//xhtml:img', XHTML_NS)
    if img is not None:
        return img.attrib['src']
    return None


def find_svg_image_old(tree):
    img = tree.find(".//svg:svg/svg:image[@xlink:href]", XHTML_NS)
    if img is not None:
        return img.attrib['{http://www.w3.org/1999/xlink}href']


def find_svg_image_new(tree):
    img = tree.find(".//svg:svg/svg:image[@href]", XHTML_NS)
    if img is not None:
        return img.attrib['href']


def get_image(xhtml_path, epub_file):
    tree = get_tree(xhtml_path, epub_file)
    img = find_img(tree)
    if img is None:
        img = find_svg_image_old(tree)
    if img is None:
        img = find_svg_image_new(tree)
    if img is not None:
        return path.join(path.dirname(xhtml_path), img)
    return None
