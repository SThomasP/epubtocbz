from xml.etree import ElementTree

ns = {
    "opf": "http://www.idpf.org/2007/opf"
}


def get_meta_xml(xml_content):
    return ElementTree.fromstring(xml_content)


def get_pages(meta_xml):
    page_list = []
    for page in meta_xml.findall("./opf:manifest/opf:item[@media-type='image/jpeg']", ns):
        page_list.append(page.attrib['href'])
    return page_list


def is_manga(meta_xml):
    reading_direction = meta_xml.find("./opf:metadata/opf:meta[@name='primary-writing-mode']", ns)
    if reading_direction is not None:
        return reading_direction.attrib['content'].endswith("rl")
