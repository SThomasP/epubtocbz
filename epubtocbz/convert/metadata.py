from xml.etree import ElementTree

ns = {
    "opf": "http://www.idpf.org/2007/opf",
    'cont': 'urn:oasis:names:tc:opendocument:xmlns:container'
}


def get_meta_xml(xml_content):
    return ElementTree.fromstring(xml_content)


def get_opf_location(container_xml):
    root_file = container_xml.find("./cont:rootfiles/cont:rootfile", ns)
    return root_file.attrib['full-path']


def get_pages(meta_xml):
    page_list = []
    for page in meta_xml.findall("./opf:manifest/opf:item[@media-type='image/jpeg']", ns):
        page_list.append(page.attrib['href'])
    return page_list


def is_manga(meta_xml):
    spine = meta_xml.find("./opf:spine", ns)
    if spine is not None and 'page-progression-direction' in spine.attrib:
        ppd = spine.attrib['page-progression-direction']
        if ppd == "rtl":
            return True
        elif ppd == "ltr":
            return False
    raise RuntimeError("Cannot determine reading direction from metadata, please specify using commandline arguments")
