# 4tim2

How To generate the modules.json file.
======================================

The module.json source file describes the modules displayed by the
configuration tool along with the addresses.csv

The source file for ABTODQ Module for the json configuration file came
from https://elmgnz.atlassian.net/wiki/display/IPC/ABTODQ+AXI+Module,
other modules can also be found there.

Each module definition has the following structure:

```
# Header (note the # is not a valid json notation)
{
	"name": "DQTOAB_AXI",  # Module name
	"instances": 1,        # The number of instances of the module.
	"registers":
	{
	# Register definitions, see below.
	}
}
```


The register definitions map directly from the module file in the Cores directory
on confluence. To convert this file to csv format, "view source" then copy and
paste into excel, Once in excel save as csv.

To convert to JSON

* Go to http://www.csvjson.com/csv2json
* Upload csv file (option1)
* Select Auto-detect and Array options


The result should look like this:
```
[
  {
    "AXI Register Name": "Config",
    "Address": 0,
    "Bit(s)": 0,
    "Sysfs file name": "go",
    "Register Format": "Bit",
    "Sysfs": "Y",
    "Cached?": "N",
    "Cache write sysfs register": "",
    "Sysfs Format": "Binary",
    "R/W": "R/W",
    "English Name": "Go bit",
    "Description": "Tells the module to perform a calculation. Also moves the cached data into the registers.",
    "Min": 0,
    "Max": 1,
    "Default": 0,
    "Step": 1,
    "Units": "unitless"
  },
  {
    "AXI Register Name": "alpha",
    "Address": "+0x10",
    "Bit(s)": "17:0",
    ....
  }
]
````

This block is pasted into the Register definitions section of the header above.

The complete modules.json file contains an array of modules
```
[
  {
  # Module 1
  },
  {
  # Modules 2
  }
]
```


Addresses.csv
-------------

The addresses.csv file provides a memory map for the modules described
in the modules.json file.

```
Address,Module Name,Module
43C00000,PIWARW_AXI_0,PIWARW_AXI
43C10000,ABTODQ_AXI_0,ABTODQ_AXI
43C20000,PIWARW_AXI_1,PIWARW_AXI
43C30000,CLKTRF_AXI_0,CLKTRF_AXI
....
```

Note: the above file maps instance 0 of PIWARW_AXI to address 43C00000
and names it PIWARW_AXI_0. Instance 1 is mapped to 43C20000.