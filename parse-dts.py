#!/usr/bin/env python

import json, os, re, sys

from collections import defaultdict
from collections import OrderedDict

#
# script description
#

help_text = '''
  {0} [/path/to/devicetree.dts]

  This script parses devicetree source to update each modules' instance
  field within the modules config file (modules.json) and generates the
  register config file (addresses.csv). This is acvieved using a regexp
  to search for the following text with the devicetree source:

  [name]: [module]_AXI@[address]

  example:
            SV3PWM_AXI_0: SV3PWM_AXI@43c40000 {{
                compatible = "elmg,sv3pwm-1.0";
                reg = <0x43c40000 0x10000>;
            }};
            CLKTRF_AXI_0: CLKTRF_AXI@43c30000 {{
                compatible = "elmg,clktrf-1.0";
                reg = <0x43c30000 0x10000>;
            }};
            PIWARW_AXI_0: PIWARW_AXI@43c00000 {{
                compatible = "elmg,piwarw-1.0";
                reg = <0x43c00000 0x10000>;
            }};
'''.format(os.path.basename(sys.argv[0]))

#
# script configuration
#

if len(sys.argv) != 2:
  print help_text
  exit(1)

dts_path = sys.argv[1]
csv_path = "addresses.csv"
json_path = "modules.json"

if not os.path.isfile(dts_path):
  print "error: invalid dts"
  exit(1)

if not os.path.isfile(json_path):
  print "error: invalid json"
  exit(1)

dts_regexp = r'\s*(\w*)\s*:\s*(\w*_AXI)@([0-9a-fA-F]*)'
csv_entries = []
json_count = defaultdict(lambda:0)


#
# parse devicetree source
#

with open(dts_path, 'r') as dts_file:
  dts_src = dts_file.read()

for match in re.findall(dts_regexp, dts_src):
  name = match[0] ; module = match[1] ; address = match[2]
  entry = "{0},{1},{2}".format(address.upper(), name, module)
  csv_entries.append(entry)
  json_count[module] += 1

#
# generate addresses.csv 
#

with open(csv_path, 'w') as csv_file:
  csv_file.write("Address,Module Name,Module\n")
  csv_file.write("\n".join(sorted(csv_entries)))

#
# parse and update modules.json
#

with open(json_path, 'r') as json_file:
  json_src = json.load(json_file, object_pairs_hook=OrderedDict)

for module in json_count:
  def each_json_mod(module):
    for json_mod in json_src:
      if json_mod['name'] == module:
        json_mod['instances'] = json_count[module]
        return
    print "warning: no definition for module {0} in {1}".format(module, json_path)
  each_json_mod(module)

with open(json_path, 'w') as json_file:
  json.dump(json_src, json_file, indent=2, sort_keys=False, separators=(',', ': '))