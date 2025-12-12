convert the input csv file as XML output

# data/template_*.xml

The templates shows the xml format. Here you need to fill the code pieces inside every value. That the code will read the xml format and modify the content according to csv entry. And create new XML files. The functions used inside XML files are stored in ComplexFunctionForColumn.py. I performed "exec()" to execute string.

## kind_of_parts.csv
Downloaded from [useful-scripts](https://gitlab.cern.ch/hgcal-database/usefull-scripts/-/blob/master/data/kind_of_parts.csv)

# Usage
```
make help
```
You will be hinted how to run this code



## ToDo list
- [ ] Upload collectLDO_v3A.csv
Checking LDO and HGCROC on CMSR
- [ ] Upload collectLDO_v3B.csv
Checking LDO and HGCROC on CMSR or not.
- [x] Upload collectLDO_v3C.csv



## installation
pip install requests
