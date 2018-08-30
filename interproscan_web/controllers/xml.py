import xml.etree.ElementTree as ET
import logging

from interproscan_web.controllers.sequence import get_sequence_id


_log = logging.getLogger(__name__)


def split_proteins(path):

    ns_uri = "http://www.ebi.ac.uk/interpro/resources/schemas/interproscan5"
    ET.register_namespace("", ns_uri)

    ns_map = {
        'p': ns_uri
    }

    tree = ET.parse(path)
    output = {}
    for protein in tree.getroot().findall('p:protein', namespaces=ns_map):
        sequence = protein.find('p:sequence', namespaces=ns_map).text
        matches = ET.Element('protein-matches')
        matches.append(protein)

        indent_xml(matches)

        sequence_id = get_sequence_id(sequence)
        output[sequence_id] = ET.tostring(matches).decode('ascii')

    return output


def indent_xml(elem, level=0):
    """makes sure the xml tree becomes a formatted text file,
       not just a single line
    """

    s = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = s + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = s
        for elem in elem:
            indent_xml(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = s
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = s

