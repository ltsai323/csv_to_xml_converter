import csv

# Input CSV file path
csv_files = [
        '../../hi.csv'
]


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
# Write IC values to a text file
    with open(output_txt_file, "w", encoding='utf-8') as txtfile:
        for value in ic_values:
            txtfile.write(value + "\n")

if __name__ == "__main__":
    rec_ldo = []
    rec_ic  = []
    for csvF in csv_files:
        ics = extract_value(csvF, columns_ic)
        LDOs = extract_value(csvF, columns_LDO)

        rec_ic.extend(ics)
        rec_ldo.extend(LDOs)

    rec_list('record_LDO.txt', rec_ldo)
    rec_list('record_ic.txt', rec_ic)
