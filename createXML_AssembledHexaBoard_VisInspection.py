import xml.etree.ElementTree as ET
import ComplexFunctionForColumn

def xml_to_dict(xml_content):
    def parse_element(element):
        # Parse an XML element and convert to dictionary recursively
        children = list(element)
        if not children:
            # Leaf node
            return element.text.strip() if element.text else None
        else:
            # Internal node
            result = {}
            for child in children:
                child_key = child.tag
                child_value = parse_element(child)
                if child_key in result:
                    # Handle repeated tags as a list
                    if not isinstance(result[child_key], list):
                        result[child_key] = [result[child_key]]
                    result[child_key].append(child_value)
                else:
                    result[child_key] = child_value
            return result

    root = ET.fromstring(xml_content)
    return {root.tag: parse_element(root)}

def dict_to_xml(input_dict, root_tag):
    """
    Converts a dictionary to an XML string.
    
    Args:
        input_dict (dict): The dictionary to convert.
        root_tag (str): The root tag for the XML.
    
    Returns:
        str: The generated XML string.
    """
    def build_element(parent, data, listKEY=None):
        """
        Recursively builds XML elements from a dictionary.
        """
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, list):
                    build_element(parent, value, key)
                else:
                    child = ET.SubElement(parent, key)
                    build_element(child, value)
        elif isinstance(data, list):
            for item in data:
                # Create individual elements for each list item using parent tag
                child = ET.SubElement(parent, listKEY)  # Correctly add siblings
                child.attrib.update( {'mode': 'auto'} )
                build_element(child, item)
        else:
            if data is not None:
                parent.text = str(data)
    
    root = ET.Element(root_tag)
    build_element(root, input_dict)
    return root

def modify_all_elements(data):
    """
    Recursively modifies all elements in a dictionary or list while retaining the structure.
    
    Args:
        data (dict | list): The input dictionary or list to process.
        
    Returns:
        dict | list | any: The modified dictionary, list, or value.
    """
    if isinstance(data, dict):
        return {key: modify_all_elements(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [modify_all_elements(item) for item in data]
    else:
        try:
            if data == None: return None
            ### If the string is a code piece, use it
            #return eval(data, {'__builtins__': None}, vars(ComplexFunctionForColumn))
            return eval(data, {}, vars(ComplexFunctionForColumn))
        except SyntaxError as e:
            ### Put the string if the interpretion failed
            return data
        except TypeError as e:
            if '(' in data and "'" in data:
                print(f'[WARNING] Save string "{ data }" to XML file without interpreting.')
            return data
        except NameError as e:
            ### Put the string if the interpretion failed
            if '(' in data and "'" in data:
                print(f'[WARNING] Save string "{ data }" without interpreting.')
            return data

import csv
def show_first_10_lines(csvFILE:str):
    '''
    Show first 10 lines for checking the startIdx filled in the further function.
    Since the first few lines being csv column definition, you need to manually
    set the number of start index.

    Args:
        csvFILE(str): input csv file
    '''

    print('[ShowColumns] Show 10 lines to set startIdx\n\n\n')
    with open(csvFILE, 'r') as f:
        reader = csv.reader(f)
        for idx, line in enumerate(reader):
            if idx == 10: break
            print(f'[Line {idx}] {line}')
    exit()

def get_value_from_key(data, target_key):
    """
    Recursively searches for a value associated with a given key in a nested dictionary.

    Args:
        data (dict): The nested dictionary to search.
        target_key (str): The key to search for.

    Returns:
        Any: The value associated with the target key, or None if not found.
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if key == target_key:
                return value
            if isinstance(value, (dict, list)):
                result = get_value_from_key(value, target_key)
                if result is not None:
                    return result
    ### ignore value in list
    #elif isinstance(data, list):
    #    for item in data:
    #        result = get_value_from_key(item, target_key)
    #        if result is not None:
    #            return result
    return None

def GetArg(argv):
    def print_help():
        raise IOError(f'''
        Input a csv file to modify template xml according csv entry.

        Args:
            arg1(str): csv file path
            arg2(int): start index of csv entry.
                       Set to 0 or negative value to show first 10 lines without modify XML template.
            ''')
    try:
        filename = argv[1]
        import os
        if not os.path.isfile(filename):
            print_help()
    except IndexError as e:
        print_help()
    startIDX = int(argv[2]) if len(argv) > 2 else 0
    return filename, startIDX

def main_func( inCSVfile:str, startIDX:int, xmlTEMPLATE:str, outputTAG:str, kopSOURCEfile:str ):
    import IOMgr_CSVinXMLout
    ComplexFunctionForColumn.init_csv_column_definition(inCSVfile, startIDX)
    ComplexFunctionForColumn.init_kind_of_part_searcher(kopSOURCEfile)
    with open(xmlTEMPLATE, 'r') as fIN:
        xml_dict_template = xml_to_dict(fIN.read())

    with open(inCSVfile, 'r') as csvFile:
        reader = csv.reader(csvFile)
        for idx, line in enumerate(reader):
            if idx < startIDX: continue # skip the column definition lines
            ComplexFunctionForColumn.set_csv_entry(line)
            xml_dict = modify_all_elements(xml_dict_template)


            ## Print the result
            PRINT_RESULT = False
            if PRINT_RESULT:
                import pprint
                pprint.pprint(xml_dict, compact=True, width=200)


            ### Build XML formated objects from dict
            xml_root = dict_to_xml(xml_dict["ROOT"], 'ROOT')
            # Save XML to a file from SERIAL_NUMBER
            serialNumber = get_value_from_key(xml_dict, "SERIAL_NUMBER")
            output_file = f'outputs/NTU_{outputTAG}_{serialNumber}.xml'
            IOMgr_CSVinXMLout.save_as_a_butified_xml_file(xml_root, output_file)
            print(f"[Output] XML file saved to {output_file}")






if __name__ == "__main__":
    import sys
    inCSVfile,startIDX = GetArg(sys.argv)
    #inCSVfile,startIDX = ('data/testsample_createXML_HexaBoard_Assembly.csv', 1)

    if startIDX<=0: show_first_10_lines(inCSVfile)

    kopSOURCE = 'data/Kind_of_parts.csv'
    xmlTEMPLATE = 'data/template_AssembledHexaboard_VisInspection.xml'
    outputTAG = 'AssembledHexBoard_VisInspection'

    main_func(
            inCSVfile = inCSVfile,
            startIDX = startIDX,
            xmlTEMPLATE = xmlTEMPLATE,
            outputTAG = outputTAG,
            kopSOURCEfile = kopSOURCE
            )
