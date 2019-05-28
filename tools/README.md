# Data Models Tools

These tools allow to automate certain tasks related to the FIWARE Data Models:

* `normalized2LD.py` allows to convert an NGSI v2 Entity represented using the normalized format into an NGSI-LD Entity (JSON-LD). It takes as input a JSON file and generates a JSON-LD file. 

* `keyValues2Normalized.py` allows to convert an NGSI v2 Entity encoded as "key-values" into an NGSI v2 Entity represented using the normalized format (i.e. Entity-Attribute-Metadata). It takes as input a JSON file and generates another JSON file. 

* `ldcontext_generator.py` extracts all the properties from each JSON Schema associated to a Data Model and generates the corresponding LD @context. The tool can be executed against the data models root folder as it will automatically scan all the directories. 
