import csv




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



def mainfunc( columnNAMEs, inCSVfile, outTEXTfile ):
    print(f'[InputCSV] {inCSVfile}')
    rec_list(outTXTfile, extract_value(inCSVfile, columnNAMEs))
    print(f'[OutputText] {outTEXTfile}')
    
    
if __name__ == "__main__":
    import sys
    ### python3 this.py iCSV.csv hiiii 'LDO1,LDO2,LDO3'

    inCSVfile = sys.argv[1]
    oTAG = sys.argv[2]
    columnNAMEs = sys.argv[3].split(',') ## column name separated by ',' like 'IC1,IC2,IC3,IC4,IC5,IC6'
    outTXTfile = f'recordValue_inCSV_{oTAG}.txt'
    mainfunc(columnNAMEs, inCSVfile, outTXTfile)
