from os import path
from xml.etree import ElementTree

XHTML_NS = {
    'xhtml': 'http://www.w3.org/1999/xhtml'
}


def get_tree(xhtml_path, epub_file):
    return ElementTree.fromstring(epub_file.read(xhtml_path).decode('utf-8'))


def get_image(xhtml_path, epub_file):
    tree = get_tree(xhtml_path, epub_file)
    img = tree.find('**/xhtml:img', XHTML_NS)
    if img is None:
        return None
    return path.join(path.dirname(xhtml_path), img.attrib['src'])