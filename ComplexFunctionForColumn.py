#!/usr/bin/env python3
import csv
def info(mesg):
    print(f'i@ {mesg}')
def warning(mesg):
    print(f'W@ {mesg}')
DEBUG_MODE = False
def BUG(mesg):
    if DEBUG_MODE:
        print(f'b@ {mesg}')

from collections import namedtuple
csv_column = namedtuple('csv_column', 'iLAYER columnNAME') # named tuple used as dict key.
CSV_COLUMN_MAPTO_IDX = {}
LOADED_CSV_COLUMNS = []
LOADED_CSV_ENTRY = []

def csv_column_idx( csvCOLUMN:csv_column ):
    '''
    Convert csv column(layer, columnNAME)  to index used to load csv entry
    This function uses csv_column as a key and get the related column_index.
    The csv_column - column_index pair is stored in CSV_COLUMN_MAPTO_IDX.
    The column_index is a mapping from LOADED_CSV_COLUMNS, so you need to fill content of
    LOADED_CSV_COLUMNS before execute this function. (Use init_csv_column_definition())

    Args:
        csvCOLUMN(csv_column): A named tuple contains csv column name and the layer index.
    '''
    global CSV_COLUMN_MAPTO_IDX
    ### if column is not listed in key, search column definition
    if csvCOLUMN not in CSV_COLUMN_MAPTO_IDX:
        try:
            idx =  LOADED_CSV_COLUMNS[csvCOLUMN.iLAYER].index(csvCOLUMN.columnNAME)
        except AttributeError as e:
            raise RuntimeError(f'[NotInitialized] LOADED_CSV_COLUMNS is not initailized, consider to use init_csv_column_definition() before execute this function\n\n\n')
        except IndexError as e:
            raise RuntimeError(f'[OutOfRange] LOADED_CSV_COLUMNS(size={len(LOADED_CSV_COLUMNS)}) rejects the access from csvCOLUMN(iLAYER={csvCOLUMN.iLAYER},columnNAME={csvCOLUMN.columnNAME})')
        CSV_COLUMN_MAPTO_IDX[csvCOLUMN] = idx

    return CSV_COLUMN_MAPTO_IDX[csvCOLUMN]


def testfunc_csv_column_idx():
    global LOADED_CSV_COLUMNS

    LOADED_CSV_COLUMNS = [
        ['CERN ID', 'myNumber','',''],
        ['hexNUM', 'hexWeig', 'hex Mass', 'hexPt'],
    ]
    my_column = csv_column(0, 'CERN ID')
    theIDX = csv_column_idx(my_column)
    info(f'[testResult] {theIDX == 0}')
    exit()

def init_csv_column_definition(csvFILE:str, evtSTARTidx:int):
    '''
    set value of LOADED_CSV_COLUMNS from input csv file.
    The content of LOADED_CSV_COLUMNS is a list containing first few lines of csv column.

    Args:
        csvFILE(str): File path of input csv data.
        evtSTARTidx(int): Index of start entry.
                          The column definition is separated at the first few lines in the csv file.
                          This variable uses this index to set the first few lines into LOADED_CSV_COLUMNS
    '''

    global LOADED_CSV_COLUMNS
    LOADED_CSV_COLUMNS = []
    with open(csvFILE, 'r') as ifile:
        reader = csv.reader(ifile)
        for i,row in enumerate(reader):
            if i > evtSTARTidx+1: # additional one line preventing error
                break
            LOADED_CSV_COLUMNS.append(row)

def testfunc_init_csv_column_definition():
    inFILE = 'test.csv'
    startIDX=5
    set_csv_column_definition(inFILE,startIDX)

    my_column_idx1 = csv_column(0, 'Batch number')
    my_column_idx5 = csv_column(2, '拍照')
    idx1 = csv_column_idx(my_column_idx1)
    idx5 = csv_column_idx(my_column_idx5)
    info(f'[testResult] {idx1==1 and idx5==5}')
    exit()

def set_csv_entry(csvENTRY):
    '''
    If you got csv entry, you can set it to global variable.
    Such as the every function is able to get this entry
    
    Args:
        csvENTRY: csv entry got from for loop
    '''
    global LOADED_CSV_ENTRY
    LOADED_CSV_ENTRY = csvENTRY
def get_value_from_csv_entry(idx:int):
    '''
    Get value from LOADED_CSV_ENTRY from index

    Args:
        idx(int): index from csv entry
    '''

    try:
        return LOADED_CSV_ENTRY[idx]
    except IndexError as e:
        raise RuntimeError(f'[NotInitialized] LOADED_CSV_ENTRY is not initialized, used set_csv_entry() before call this function')
def testfunc_read_csv_entry():
    inFILE = 'test.csv'
    startIDX = 5

    init_csv_column_definition(inFILE, startIDX)

    my_column_idx1 = csv_column(0, 'Batch number')
    my_column_idx5 = csv_column(2, '拍照')
    idx1 = csv_column_idx(my_column_idx1)
    idx5 = csv_column_idx(my_column_idx5)
    with open(inFILE, 'r') as f:
        reader = csv.reader(f)
        info(type(reader))

        for lineIdx, line in enumerate(reader):
            if lineIdx < startIDX: continue
            set_csv_entry(line)
            info(f'[Entry] batch number {get_value_from_csv_entry(idx1)} and photo {get_value_from_csv_entry(idx5)}')

def CSV_COLUMN(iLAYER:int,columnNAME:str):
    idx = csv_column_idx( csv_column(iLAYER=iLAYER, columnNAME=columnNAME) )
    return get_value_from_csv_entry(idx)

def CheckEqualValue(iLAYER:int,columnNAME:str,equalVALUE:str):
    val = CSV_COLUMN(iLAYER,columnNAME)
    if val == equalVALUE: return None # Pass checking
    ### if the value is not wanted value, show message
    return f'[InvalidValue] "{ columnNAME }" got value "{ val }". Which is expected as "{ equalVALUE }"'

def MergeStatus( *statusLIST ) -> str:
    available_messages = [ status for status in statusLIST if status ]
    if len(available_messages) == 0: return ''
    return '. ' + ', '.join(available_messages)




import datetime
def TimeStamp():
    return str(datetime.datetime.now())

def get_time(timeSTR):
    try:
        return datetime.datetime.strptime(timeSTR, '%Y-%m-%d %H:%M:%S')
    except ValueError as e:
        pass
    try:
        return datetime.datetime.strptime(timeSTR, '%Y.%m.%d')
    except ValueError as e:
        pass
    try:
        return datetime.datetime.strptime(timeSTR, '%Y:%m:%d')
    except ValueError as e:
        pass
    try:
        return datetime.datetime.strptime(timeSTR, '%Y/%m/%d')
    except ValueError as e:
        pass
    info(f'[PatternRecognizationFailed] Input string "{ timeSTR }" cannot be converted to timestemp. Use current time')
    return datetime.datetime.now()
def TimeStampConv(timeSTAMP:str):
    return get_time(timeSTAMP)

class kind_of_part_mapping:
    def __init__(self, csvFILE):
        with open(csvFILE, 'r') as f:
            reader = csv.DictReader(f)
            self.entries = []
            for entry in reader:
                code = entry['label_typecode'].upper().replace('-','')
                entry['code'] = code
                self.entries.append(entry)
            #self.entries = [ entry for entry in reader ]
        info(f'[Initialized] kind_of_part_mapping() correctly activated')
    def Get(self, barcode):
        if '320' != barcode[0:3]: raise IOError(f'[InvalidBarcode] {barcode}')
        
        try:
            barcode_piece = barcode[3:-5]
            if len(barcode_piece) < 2: raise IndexError()
        except IndexError as e:
            raise IndexError(f'\n\n[InvalidBARCODE] input barcode "{barcode}" cannot get correct barcode piece from barcode[3:-5]\n\n') from e
        for entry in self.entries:
            if entry['code'] in barcode_piece:
                if entry['code'] == "": continue
                BUG(f'[SearchRes] KindOfPart got barcode "{barcode_piece}" matching "{entry["code"]}" so the result is "{entry["display_name"]}"')
                return entry['display_name']
kindofpart_sources = None
def init_kind_of_part_searcher(kindOFpartsCSV:str):
    global kindofpart_sources
    kindofpart_sources = kind_of_part_mapping(kindOFpartsCSV)

def FindKindOfPart(BARCODEorSERIALNUMBER:str):
    global kindofpart_sources
    try:
        return kindofpart_sources.Get(BARCODEorSERIALNUMBER)
    except AttributeError as e:
        raise RuntimeError(f'[FindKindOfPart] kindofpart_sources is not initialized, Use init_kind_of_part_searcher() before use this function\n\n\n')

def testfunc_FindKindOfPart():
    kop_file = 'data/Kind_of_parts.csv'
    init_kind_of_part_searcher(kop_file)

    serial_number = '320070100300068'
    info(FindKindOfPart(serial_number))
    exit()

    



def ReplaceBoolToPass(v):
    try:
        if v.lower() == 'true':
            return 'Pass'
    except ValueError as e:
        warning(f'[ValueError] "{ v }" is not a str, a false recorded in event.')
    return 'Fail'

def FlatnessGrading(v):
    new_val = 'invalid'
    if '<0.50'   == v: new_val = 'Pass'
    if '0.5~1.0' == v: new_val = 'Pass'
    if '>1.0'    == v: new_val = 'Fail'

    if new_val == 'invalid':
        info(f'[InvalidFlatnessGrading] Unable to recognize flatness "{ v }" from string.')
        new_val = 'Fail'
    BUG(f'[FlatnessGrading] Got comment "{ v }" so grading "{ new_val }" given.')
    return new_val
def grading(*vLIST):
    return 'Pass'
    #return f'[grading] {[v for v in vLIST]}'

def ICID(v):
    try:
        id_list = v.split(' ')
        return f'{id_list[1]}-{id_list[0]}'
    except IndexError as e:
        raise RuntimeError(f'[Invalid IC ID] input ID "{ v }" in wrong format. Please check it')


if __name__ == "__main__":
    #testfunc_csv_column_idx()
    #testfunc_init_csv_column_definition()
    testfunc_read_csv_entry()
    #testfunc_FindKindOfPart()

