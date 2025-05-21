import csv


# Columns to extract
columns_ic = ["IC1", "IC2", "IC3", "IC4", "IC5", "IC6"]
columns_LDO = ["LDO1","LDO2","LDO3"]


# Read CSV and extract IC values
def extract_value(csv_file, ic_columns):
    ic_values = []
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for ic in ic_columns:
                if row.get(ic) and row[ic].strip():  # Ensure the value is not empty
                    ic_values.append(row[ic].strip())
    return ic_values

def rec_list(output_txt_file, ic_values):
# Use a set to track seen strings
    seen = set()

# Write IC values to a text file
# Open the file in write mode
    with open(output_txt_file, 'w') as txtfile:
        for value in ic_values:
            if value not in seen:  # Check if the string is already recorded
                txtfile.write(value + '\n')  # Write the string to the file
                seen.add(value)  # Add string to the set of seen strings



def extractColumn(inCSV, outTEXT, columnDEF:list):
    print(f'[InputCSV] {inCSV}')
    rec_list(outTXTfile, extract_value(inCSVfile, columnDEF))
    print(f'[OutputText] {outTEXT}')
    
def mainfunc( mode, inCSVfile, outTEXTfile ):
    column = None
    if mode == 'LDO':
        column = columns_LDO
        print('a')
    if mode == 'HGCROC':
        column = columns_ic
        print('b')
    if mode == None:
        raise IOError(f'[Invalid option] mode "{mode}" is invalid. Only support "LDO" and "HGCROC"')

    print(f'mode: {mode}')
    print(f'column: {column}')
    extractColumn(inCSVfile, outTEXTfile, column)
    
if __name__ == "__main__":
    import sys

    mode = sys.argv[1]
    oTAG = sys.argv[2]
    inCSVfile = sys.argv[3]
    outTXTfile = f'record_{oTAG}_{mode}.txt'
    mainfunc(mode, inCSVfile, outTXTfile)
