# 4tim2

CVS -> JSON Conversion.


1. Export file as csv in edit mode select and copy table.
2. go to http://www.csvjson.com/csv2json
3. Upload csv file (option1)
4  Select Auto-detect and Array options
5 Copy into module.json with header 

Befor the last line "}]"

Add


, {
	"name": "DQTOAB_AXI",
	"instances": 1,
	"registers":
	
	
Then paste the json output.

[lots of stuff]



The last line should still be "}]"

