from lxml import etree

class XmlReader(object):
    def __init__(self, file_name, xpath='/DATA/ROW'):
        self.filename = file_name 
        self.xpath = xpath

    def read(self):
        root = etree.parse(self.filename)
        for node in root.xpath(self.xpath):
            yield node 


def elemtext(node, path):
    if node is None:
        return None
    elem = node.find(path)
    if elem is not None and elem.text: 
        return elem.text.strip()
    else:
        return None

def fieldval(node, field):
    val = elemtext(node, field)
    if val and val not in ['NULL',]:
        return val
