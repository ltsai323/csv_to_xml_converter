import xml.etree.ElementTree as ET
import xml.dom.minidom

def create_nested_xml(data: dict, root_name="ROOT"):
    """
    Convert a dictionary with keys as paths to an XML structure.

    Args:
        data (dict): The dictionary where keys are paths like "folder1/folder2/name".
        root_name (str): The name of the root element in the XML.
    Returns:
        xml.etree.ElementTree.Element: Root element of the XML structure.
    """
    root = ET.Element(root_name)

    for path, value in data.items():
        # Split the key by '/' to determine the hierarchy
        parts = path.split('/')
        current = root

        # Navigate or create the nested structure
        for part in parts[:-1]:  # Traverse all except the last part
            # Find an existing sub-element with the same tag, or create a new one
            found = current.find(part)
            if found is None:
                found = ET.SubElement(current, part)
            current = found

        # Add the final part as a tag and set its text content
        ET.SubElement(current, parts[-1]).text = str(value)

    return root

def save_to_xml_file(root, filename):
    """
    Save the XML structure to a file.

    Args:
        root (xml.etree.ElementTree.Element): Root element of the XML structure.
        filename (str): The filename to save the XML file.
    """
    tree = ET.ElementTree(root)
    tree.write(filename, encoding="utf-8", xml_declaration=True)

def save_as_a_butified_xml_file(xmlELEMENT:ET.Element, xmlFILE:str):
    # Convert the ElementTree to a string
    xml_str = ET.tostring(xmlELEMENT, encoding='utf-8', method='xml')

    # Pretty-print using minidom
    dom = xml.dom.minidom.parseString(xml_str)
    pretty_xml_as_string = dom.toprettyxml(indent="  ")

    # Write to the XML file
    with open(xmlFILE, 'w') as xml_out:
        xml_out.write(pretty_xml_as_string)


    #print(f"XML file '{xmlFILE}' has been created successfully.")

# Example usage
if __name__ == "__main__":
    # Sample input dictionary
    input_data = {
        "folder1/folder2/name": "John Doe",
        "folder1/folder2/age": "30",
        "folder1/folder3/item1": "Value1",
        "folder1/folder3/item2": "Value2",
        "folder4/attribute": "SomeAttribute"
    }

    # Generate XML structure
    xml_root = create_nested_xml(input_data, 'ROOT')

    # Save XML to a file
    #save_to_xml_file(xml_root, "output.xml")
    save_as_a_butified_xml_file(xml_root, "output.xml")

    print("XML file 'output.xml' has been created.")
