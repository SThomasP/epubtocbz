from xml.etree import ElementTree

CONTAINER_NS = {
    'cont': 'urn:oasis:names:tc:opendocument:xmlns:container'
}


def get_opf_file_location(epub_file):
    container_xml = ElementTree.fromstring(epub_file.read("META-INF/container.xml").decode('utf-8'))
    return get_opf_location(container_xml)


def get_opf_location(container_xml):
    root_file = container_xml.find("./cont:rootfiles/cont:rootfile", CONTAINER_NS)
    return root_file.attrib['full-path']
