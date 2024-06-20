import xml.etree.ElementTree as ET
from difflib import unified_diff

def read_xml(file_path):
    tree = ET.parse(file_path)
    return tree.getroot()

def xml_to_string(element):
    return ET.tostring(element, encoding='unicode')

def compare_xml(file1, file2):
    xml1 = read_xml(file1)
    xml2 = read_xml(file2)

    xml1_str = xml_to_string(xml1)
    xml2_str = xml_to_string(xml2)

    #print("XML 1 Content:")
    #print(xml1_str)
    #print("XML 2 Content:")
    #print(xml2_str)

    diff = unified_diff(
        xml1_str.splitlines(keepends=True),
        xml2_str.splitlines(keepends=True),
        fromfile=file1,
        tofile=file2
    )

    diff_output = ''.join(diff)
    if not diff_output:
        print("No differences found.")
    return diff_output

if __name__ == "__main__":
    file1 = './files/admin_PROD.xml'
    file2 = './files/admin_TEST.xml'
    differences = compare_xml(file1, file2)
    print(f"Len {len(differences)}")
    
    if len(differences.split()) > 0:
        f = open("differences_output.txt","w")
        f.write(f"Differences:\n\n{differences}")
        f.close
    else:
        print("Nothing to write.")