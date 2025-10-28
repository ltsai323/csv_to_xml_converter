#!/usr/bin/env python3
import logging
import sys

log = logging.getLogger(__name__)
import os
DEBUG_MODE = True if os.environ.get('LOG_LEVEL', 'INFO') == 'DEBUG' else False

import csv


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
    log.info(f'[testResult] {theIDX == 0}')
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
    log.info(f'[testResult] {idx1==1 and idx5==5}')
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
        log.info(type(reader))

        for lineIdx, line in enumerate(reader):
            if lineIdx < startIDX: continue
            set_csv_entry(line)
            log.info(f'[Entry] batch number {get_value_from_csv_entry(idx1)} and photo {get_value_from_csv_entry(idx5)}')

def CSV_COLUMN(iLAYER:int,columnNAME:str):
    idx = csv_column_idx( csv_column(iLAYER=iLAYER, columnNAME=columnNAME) )
    return get_value_from_csv_entry(idx)

def CheckEqualValue(iLAYER:int,columnNAME:str,equalVALUEs:list):
    val = CSV_COLUMN(iLAYER,columnNAME)

    passed = False
    for equalVALUE in equalVALUEs:
        if val == equalVALUE:
            passed = True
            break
    if passed: return None # Pass checking
    ### if the value is not wanted value, show message
    return f'[InvalidValue] "{ columnNAME }" got value "{ val }". Which is expected as "{ equalVALUE }"'

def MergeStatus( *statusLIST ) -> str:
    available_messages = [ status for status in statusLIST if status ]
    if len(available_messages) == 0: return ''
    return '. ' + ', '.join(available_messages)




import datetime
import locale
def TimeStamp():
    return str(datetime.datetime.now())

def get_time(timeSTR):
    try:
        return datetime.datetime.strptime(timeSTR, '%Y-%m-%d %H:%M:%S')
    except ValueError as e: pass
    try:
        return datetime.datetime.strptime(timeSTR, '%Y-%m-%d')
    except ValueError as e: pass
    try:
        return datetime.datetime.strptime(timeSTR, '%Y.%m.%d')
    except ValueError as e: pass
    try:
        return datetime.datetime.strptime(timeSTR, '%Y:%m:%d')
    except ValueError as e: pass
    try:
        return datetime.datetime.strptime(timeSTR, '%Y/%m/%d')
    except ValueError as e: pass
    try:
        locale.setlocale(locale.LC_TIME, 'zh_TW.UTF-8')
        return datetime.datetime.strptime(timeSTR, "%Y/%m/%d %p %I:%M:%S")
    except ValueError as e: pass
    #except ValueError as e:
    #    raise ValueError(f'unable to get time from "{timeSTR}"') from e

    log.info(f'[PatternRecognizationFailed] Input string "{ timeSTR }" cannot be converted to timestemp. Use current time')
    return datetime.datetime.now()
def TimeStampConv(timeSTAMP:str):
    return get_time(timeSTAMP)
RUN_NUMBER_LOCATION = { 'NTU': '2601' }
def RunNumberGenerator(location:str, timeSTAMP ):
    if location not in RUN_NUMBER_LOCATION.keys():
        ''' Check location code here https://int2r-shipment.web.cern.ch/locations/ '''
        raise NotImplementedError(f'[InvalidLocation] RunNumberGenerator() got invalid location "{ location }".')
   #now = datetime.datetime.now()
    now = timeSTAMP
    return now.strftime(f"{RUN_NUMBER_LOCATION[location]}%y%m%d%H%M%S")
def RunNumber( timeSTR ):
    return RunNumberGenerator('NTU',timeSTR)
    

    

class kind_of_part_mapping:
    def __init__(self, csvFILEs:list):
        self.entries = []
        self.codes_history = set()
        for csvFILE in csvFILEs:
            log.info(f'[LoadKindOfPart] file "{ csvFILE }" loaded.')
            with open(csvFILE, 'r') as f:
                reader = csv.DictReader(f)
                for entry in reader:
                    # load entry in CSV file and add additional column 'code'.
                    code = entry['LABEL_TYPECODE'].replace('-','')
                    if code == '': continue
                    entry['code'] = code
                    if code in self.codes_history:
                        log.warning(f'[Duplicated KindOfPart] Got duplicated code "{ code }" in entry "{ entry }". Skip it')
                        continue
                    self.entries.append(entry)
                    self.codes_history.add(code)


        log.info(f'[Initialized] kind_of_part_mapping() correctly activated')
    def Get(self, barcode):
        isLDOorHGCROC = True if '320' != barcode[0:3] else False
        
        try:
            barcode_without_number = barcode[:-4] 
            if len(barcode_without_number) < 2: raise IndexError()
        except IndexError as e:
            raise IndexError(f'\n\n[InvalidBARCODE] input barcode "{barcode}" cannot get correct barcode piece from barcode[:-5]\n\n') from e
        for entry in self.entries:
            if entry['code'] in barcode_without_number:
                if entry['code'] == "": continue
                log.debug(f'[SearchRes] KindOfPart got barcode "{barcode_without_number}" matching "{entry["code"]}" so the result is "{entry["DISPLAY_NAME"]}"')
                display_name = entry['DISPLAY_NAME']
                if isLDOorHGCROC:
                    if 'LDO' in display_name: return display_name
                    if 'HGCROC' in display_name: return display_name
                if not isLDOorHGCROC:
                    if 'LDO' not in display_name and 'HGCROC' not in display_name: return display_name

        err_mesg = f'[NoSearchResult] kind_of_part_mapping() is unable to match barcode "{ barcode }".'
        if DEBUG_MODE:
            log.debug(err_mesg)
            log.debug('[IgnoreEmptyValue] kind_of_part_mapping() puts empty value in this field.')
            return ''
        raise IOError(err_mesg)

kindofpart_sources = None
def init_kind_of_part_searcher(kindOFpartsCSVs:list):
    global kindofpart_sources
    kindofpart_sources = kind_of_part_mapping(kindOFpartsCSVs)

def FindKindOfPart(BARCODEorSERIALNUMBER:str):
    global kindofpart_sources
    try:
        return kindofpart_sources.Get(BARCODEorSERIALNUMBER)
    except AttributeError as e:
        raise RuntimeError(f'[FindKindOfPart] kindofpart_sources is not initialized, Use init_kind_of_part_searcher() before use this function\n\n\n')
def FindKindOfPartIfBarcodeExist(BARCODEorSERIALNUMBER:str):
    global kindofpart_sources
    try:
        return kindofpart_sources.Get(BARCODEorSERIALNUMBER) if BARCODEorSERIALNUMBER != '' else ''
    except AttributeError as e:
        raise RuntimeError(f'[FindKindOfPart] kindofpart_sources is not initialized, Use init_kind_of_part_searcher() before use this function\n\n\n')

def FindKindOfPart_AncientCoding(BARCODEorSERIALNUMBER:str):
    new_barcode = '320'+BARCODEorSERIALNUMBER
    return FindKindOfPart(new_barcode)

def testfunc_FindKindOfPart():
    kop_file = 'data/Kind_of_parts.csv'
    init_kind_of_part_searcher([kop_file])

    serial_number = '320070100300068'
    log.info(FindKindOfPart(serial_number))
    exit()

def testfunc_FindKindOfPart2():
    kopSOURCEfiles = ['data/Kind_of_parts.csv', 'data/Kind_of_parts_appendix.csv' ]
    init_kind_of_part_searcher(kopSOURCEfiles)

    serial_number = 'LDO 10 001463'
    log.info(FindKindOfPart(serial_number))

#### https://confluence.cern.ch/pages/viewpage.action?pageId=576651582
HGCROC_ATTRIBUTE_WITHOUT_NUMBER = {
        'LD Full': 'M',
        'LD Five': 'IC',
        'LD Left': 'M',
        'LD Right': 'M',
        'LD Top': 'IC',
        'LD Bottom': 'M',

        'HD Full': 'IC',
        'HD Left': 'IC',
        'HD Right': 'IC',
        'HD Top': 'IC',
        'HD Bottom': 'M'
        }
def FindHGCROCvalue( barcodeOFboard, HGCROCcolumnNAME):
    # barcodeOFboard records the barcode of assembled hexaboard.
    # HGCROCcolumnNAME puts "IC3". Not to put barcode of HGCROC 
    boardKOP = FindKindOfPart(barcodeOFboard)
    HGCROC_digit = int(HGCROCcolumnNAME[-1]) # last value is a number
    for board_type, HGCROCtag in HGCROC_ATTRIBUTE_WITHOUT_NUMBER.items():
        if board_type not in boardKOP: continue
        return f'{HGCROCtag}{HGCROC_digit}'
    return f'Input HGCROC "{ HGCROCcolumnNAME }" is invalid'
def FindHGCROCname( barcodeOFboard ):
    # barcodeOFboard records the barcode of assembled hexaboard.
    # the barcode is to check HD or LD
    boardKOP = FindKindOfPart(barcodeOFboard)
    if 'HD' in boardKOP: return 'HD HGCROC Position'
    if 'LD' in boardKOP: return 'LD HGCROC Position'
    return 'ERROR. FindHGCROCname() cannot get "HD" or "LD" in barcode "{barcodeOFboard}"'


LDO_ATTRIBUTE_WITHOUT_NUMBER = {
        'LD Full': 'U',
        'LD Five': 'IC',
        'LD Left': 'U',
        'LD Right': 'U',
        'LD Top': 'IC',
        'LD Bottom': 'IC',

        'HD Full': 'reg',
        'HD Left': 'IC',
        'HD Right': 'IC',
        'HD Top': 'IC',
        'HD Bottom': 'reg'
        }
def FindLDOvalue( barcodeOFboard, LDOcolumnNAME):
    # barcodeOFboard records the barcode of assembled hexaboard.
    # LDOcolumnNAME puts "LDO3". Not to put barcode of LDO
    boardKOP = FindKindOfPart(barcodeOFboard)
    LDO_digit = int(LDOcolumnNAME[-1]) # last value is a number
    for board_type, LDOtag in LDO_ATTRIBUTE_WITHOUT_NUMBER.items():
        if board_type not in boardKOP: continue
        return f'{LDOtag}{LDO_digit}'
    return f'Input LDO "{ LDOcolumnNAME }" is invalid'
    
    
    
def TranslateSensorBarcode(density:str, sensorBARCODE:str):
    ''' 600036_2 '''


    MM = None
    if density == 'HD': MM = 'SH'
    if density == 'LD': MM = 'SL'
    if MM == None: raise ValueError(f'[InvalidDensityCode] TranslateSensorBarcode() got invalid density "{ denstiy }". Only HD and LD available')


    if '_' not in sensorBARCODE:
        raise ValueError(f'[InvalidSensorBarcode] code "{ sensorBARCODE }" is invalid')
    #geoTYPE = { '0':'full', '1':'top', '2':'bottom', '3':'left', '4':'right', '5':'five' }
    geoTYPE = { '0':'FXX', '1':'TXX', '2':'BXX', '3':'LXX', '4':'RXX', '5':'5XX' }
    geocode = sensorBARCODE.split('_')[1]
    try:
        geotype = geoTYPE[geocode]
    except KeyError as e:
        raise KeyError(f'[InvalidSensorBarcode] code "{ sensorBARCODE }" got strange geometry code "{ geocode }".') from e

    #thicknessTYPE = { '1':'300um', '2':'200um', '3':'120um', '4':'300um partial','5':'200um partial', '6':'120um partial' }
    thicknessCODE =  { '1':'3'    , '2':'2'    , '3':'1'    , '4':'3'            ,'5':'2', '6':'1' }
    thicknesscode = thicknessCODE[ sensorBARCODE[0] ]
    TTTT = thicknesscode + geotype

    NNNNN = sensorBARCODE.replace('_','')
    return '320'+MM+TTTT+NNNNN
    




def ReplaceBoolToPass(v):
    try:
        if v.lower() == 'true':
            return 'Pass'
    except ValueError as e:
        log.warning(f'[ValueError] "{ v }" is not a str, a false recorded in event.')
    return 'Fail'

def FlatnessGrading(v):
    new_val = 'invalid'
    passed = [ '<0.50', '0.5', '0.5~1.0', '1.00~1.50', '<0.5', '>1.0', '0.50~1.00', '1.0~1.5' ]
    failed = [ '1.5~2.0', '2.0~1.5', '2.0~2.5', '2.5~3.0' ]

    if v in passed: new_val = 'Pass'
    if v in failed: new_val = 'Fail'

    if new_val == 'invalid':
        log.info(f'[InvalidFlatnessGrading] Unable to recognize flatness "{ v }" from string.')
        new_val = 'Fail'
    log.debug(f'[FlatnessGrading] Got comment "{ v }" so grading "{ new_val }" given.')
    return new_val
def grading(*vLIST):
    raise NotImplementedError('[grading] is a incompleted function. implement it now!')
    #return f'[grading] {[v for v in vLIST]}'

DEFINED_ICTYPE = {
        'v3b': '3b',
        'v3a': '3a',
        'v3c': '3c',
        }

def ICID(icTYPE,icID):
    try:
        if icID:
            ictype = icTYPE.lower()
            if ictype == 'v3a': return icID # asdf
            if ictype == 'v3b': return f'ICRH{DEFINED_ICTYPE[ictype]}{icID}'
            if ictype == 'v3c': return icID
            log.debug(f'[Blank ICID] type {icTYPE} and ic ID {icID} finds no matching. Empty field filled')
        else:
            log.debug(f'[NoICID] Skip this entry')
        return ''

    except KeyError as e:
        raise RuntimeError(f'[Invalid IC ID] input ID "{ v }" in wrong format. Please check it')
def FillValueIfColumnExisted(val, col):
    log.debug(f'[FillValueIfColumnExisted] got column "{col}" so return val "{val if col != "" else ""}"')
    return val if col != '' else ''

def BatchNumber(v):
    def generate_batch_number(dt=None):
        if dt is None:
            dt = datetime.datetime.now()
        
        # Extract the last two digits of the year
        year_suffix = dt.strftime('%y')  # '%y' gives the last two digits of the year, e.g., '25' for 2025
        
        # Extract the ISO week number
        # isocalendar() returns a tuple (ISO year, ISO week number, ISO weekday)
        week_number = dt.isocalendar()[1]
        
        # Format the week number as a two-digit string, adding a leading zero if necessary
        week_number_str = f"{week_number:02d}"
        
        # Combine the year suffix and week number to form the batch number
        batch_number = f"{year_suffix}{week_number_str}"
        
        return batch_number
    if DEBUG_MODE:
        if v == '':
            log.debug(f'[IgnoreEmptyValue] BatchNumber() got empty input. Put empty into field')
            return ''

    if len(v) == 4: return v
    t = get_time(v)
    return generate_batch_number(t)


OUTPUT_VERSION = '1'
def set_version(v):
    global OUTPUT_VERSION
    OUTPUT_VERSION = v
    log.info(f'[Version] Set output version as {OUTPUT_VERSION}')
def VERSION():
    global OUTPUT_VERSION
    return str(OUTPUT_VERSION)

def CheckValue_In(v:str, fragLIST:list):
    ''' check the input value in one of fragLIST
    ex:
      input value aaa in fragLIST [ "aa", "bbb" ]
    '''
    for frag in fragLIST:
        if frag in v: return True
    return False
def CheckValue_NotIn(v:str, fragLIST:list):
    ''' check the input value not in any of fragLIST
    ex:
      input value https://lka.asmdnoun.com//k not in any of fragLIST [ "https", "IGNORE" ]
    '''
    for frag in fragLIST:
        if frag in v: return False
    return True



if __name__ == '__main__':
    import os
    loglevel = os.environ.get('LOG_LEVEL', 'INFO') # DEBUG, INFO, WARNING
    DEBUG_MODE = True if loglevel == 'DEBUG' else False
    logLEVEL = getattr(logging, loglevel)
    logging.basicConfig(stream=sys.stdout,level=logLEVEL,
                        format='[basicCONFIG] %(levelname)s - %(message)s',
                        datefmt='%H:%M:%S')

    #testfunc_csv_column_idx()
    #testfunc_init_csv_column_definition()
    #testfunc_read_csv_entry()
    #testfunc_FindKindOfPart()
    testfunc_FindKindOfPart2()
