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
