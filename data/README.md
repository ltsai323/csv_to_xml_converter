# XML Template
You can check the XML template used for INT2R / CMSR uploading.
[confluence.cern.ch](https://confluence.cern.ch/display/HGCLogic/Database+structure+and+upload+procedures#Databasestructureanduploadprocedures-Protomodule&Moduleassembly)

The uploading templates are
### Create part
* bare hexaboard
* Assembled hexaboard
* ProtoModule
* SiModule

Create parts declares an new entry on database for further use. Once operator wants to assembly an advance component, the database checks the existance of related daughters.
#### Known relationships

|Component Name| Daughters   |
|--------------|-------------|
|Bare hexaboard| No daughter |
|Assembled hexaboared| bare hexaboard|
|Assembled hexaboared| HGC ROC|
|Assembled hexaboared| LDO|
|ProtoModule         | Baseplate|
|ProtoModule         | Sensor|
|SiModule            | ProtoModule|
|SiModule            | Assembled hexaboard|

### Visual Inspection
* bare hexaboard
* Assembled hexaboard
* ProtoModule
* SiModule

Visual inspection records the visual inspection of the component.


## How do I modify **template_blahblah.xml**?

**template_blahblah.xml** records the structure downloaded from [confluence.cern.ch](https://confluence.cern.ch/display/HGCLogic/Database+structure+and+upload+procedures#Databasestructureanduploadprocedures-Protomodule&Moduleassembly)
**createXML.py** reads the structure of the template and recognize the value in xml file as a piece of python code.
There are 2 rules in the xml template
1. recorded attribute in XML template will be interpret as a python code piece. You can use functions in **ComplexFunctionForColumn.py**.
2. Once the recorded attribute is not a python code, it will be considered as a constant string recorded into output xml files.
