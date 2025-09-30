#!/usr/bin/env python3
import logging
import sys
log = logging.getLogger(__name__)

import xml.etree.ElementTree as ET
import ComplexFunctionForColumn
DEBUG_MODE = False
FILE_IDENTIFIER = 'createXML.py'
def BUG(mesg):
    if DEBUG_MODE:
        print(f'b-{FILE_IDENTIFIER}@ {mesg}')



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

    print(xml_content)
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
def pass_event_filter(filterFUNCs):
    ''' every event filter is AND operation '''
    for filterFUNC in filterFUNCs:
        if eval(filterFUNC, {}, vars(ComplexFunctionForColumn)) == False:
            log.debug(f'[RejectEvent] function {filterFUNC} rejected this event')
            return False
    return True
def remove_empty_entries_from_list(nested_dict):
    """
    Remove dictionaries in a list if no barcode in this entry.

    Args:
        nested_dict (dict): The nested dictionary to process.

    Returns:
        dict: The updated dictionary with empty entries removed.
    """
    def is_dict_empty(d):
        #return all(v in [None, "", []] for v in d.values())
        return False if d.get('SERIAL_NUMBER') else True
    
    def clean_children(children):
        if isinstance(children, list):
            return [child for child in children if not is_dict_empty(child)]
        return children
    
    def recursive_clean(data):
        if isinstance(data, dict):
            for key, value in data.items():
                if key == "CHILDREN" and "PART" in value:
                    value["PART"] = clean_children(value["PART"])
                else:
                    recursive_clean(value)
        return data

    return recursive_clean(nested_dict)

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
            line_with_number = [ f'{ii}:{vv}' for ii,vv in enumerate(line) ]
            print(f'[Line {idx}] {line_with_number}')
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


def main_func( inCSVfile:str, startIDX:int, xmlTEMPLATE:str, outputTAG:str, inFILTER:str="", version:str='1' ):
    kopSOURCEfiles = ['data/Kind_of_parts.csv', 'data/Kind_of_parts_appendix.csv' ]
    import IOMgr_CSVinXMLout
    ComplexFunctionForColumn.init_csv_column_definition(inCSVfile, startIDX)
    ComplexFunctionForColumn.init_kind_of_part_searcher(kopSOURCEfiles)
    ComplexFunctionForColumn.set_version(version)
    with open(xmlTEMPLATE, 'r') as fIN:
        xml_dict_template = xml_to_dict(fIN.read())

    filter_funcs = []
    if inFILTER:
        with open(inFILTER,'r') as filterIN:
            for line in filterIN.readlines():
                filter_funcs.append(line.strip())

    with open(inCSVfile, 'r') as csvFile:
        reader = csv.reader(csvFile)
        for idx, line in enumerate(reader):
            if idx < startIDX: continue # skip the column definition lines
            ComplexFunctionForColumn.set_csv_entry(line)
            if not pass_event_filter(filter_funcs): continue
            xml_dict_contains_empty = modify_all_elements(xml_dict_template)
            xml_dict = remove_empty_entries_from_list(xml_dict_contains_empty)


            if DEBUG_MODE:
                import pprint
                pprint.pprint(xml_dict, compact=True, width=200)


            ### Build XML formated objects from dict
            xml_root = dict_to_xml(xml_dict["ROOT"], 'ROOT')
            # Save XML to a file from SERIAL_NUMBER
            serialNumber = get_value_from_key(xml_dict, "SERIAL_NUMBER")
            output_file = f'outputs/NTU_{outputTAG}_{serialNumber}.xml'
            IOMgr_CSVinXMLout.save_as_a_butified_xml_file(xml_root, output_file)
            print(f"[Output] XML file saved to {output_file}")

            #if DEBUG_MODE:
            #    BUG(f'[DEBUG MODE] Only show one entry for checking')
            #    break




if __name__ == '__main__':
    import os
    loglevel = os.environ.get('LOG_LEVEL', 'INFO') # DEBUG, INFO, WARNING
    DEBUG_MODE = True if loglevel == 'DEBUG' else False
    logLEVEL = getattr(logging, loglevel)
    logging.basicConfig(stream=sys.stdout,level=logLEVEL,
                        format='[basicCONFIG] %(levelname)s - %(message)s',
                        datefmt='%H:%M:%S')


    xmlTEMPLATE = sys.argv[1]
    inCSVfile   = sys.argv[2]
    outputTAG   = sys.argv[3]
    inFILTER    = "" if len(sys.argv) < 4+1 else sys.argv[4]
    startIDX    = 1 if len(sys.argv) < 5+1 else int(sys.argv[5])

    
    if startIDX<=0: show_first_10_lines(inCSVfile)

    outputVERSION = '1'


    main_func(
            inCSVfile = inCSVfile,
            startIDX = startIDX,
            xmlTEMPLATE = xmlTEMPLATE,
            outputTAG = outputTAG,
            inFILTER = inFILTER,
            version = outputVERSION
            )
