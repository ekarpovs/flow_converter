# Usage:
#   python run.py -w <worksheet full name> -o <output file> [-t no/yes]
# 

import argparse
import json

from flow_converter import FlowConverter

# Construct the argument parser and parse the arguments
def parseArgs():
  ap = argparse.ArgumentParser(description="flow converter")
  ap.add_argument("-w", "--wrk", required = True,
	help = "full path to the meta data file")
  ap.add_argument("-o", "--output", required = True,
	help = "full path to the output file(s)")
  ap.add_argument("-t", "--trace", required = False,
  default="no",
	help = "print output")
  
  args = ap.parse_args()   
  kwargs = dict((k,v) for k,v in vars(args).items() if k!="message_type")
  return kwargs


# Reads the string from the file, parses the JSON data, 
# populates a Python dict with the data
def readJson(ffn):
  with open(ffn, 'rt') as f:
    data = json.load(f)
  return data

def storeFsmDef(out_path, fsm_def):
  ffn = "{}/fsm-def.json".format(out_path)
  json_object = json.dumps(fsm_def, indent = 2) 
  with open(ffn, "w") as outfile: 
    outfile.write(json_object)
  return


# Main function
def main(**kwargs): 
  worksheet = readJson(kwargs.get('wrk'))
  worksheet.append({"stm": "glbstm.end"})
  for i, meta in enumerate(worksheet):
    meta['id'] = i
  # usage in a client - begin
  fc = FlowConverter(worksheet)
  fsm_def = fc.convert()
  # usage in a client - end
  
  output_path = kwargs.get('output', '../data/fsm-def')
  if kwargs.get('trace', 'no') == 'yes':
    storeFsmDef(output_path, fsm_def)

# Entry point
if __name__ == "__main__":
    kwargs = parseArgs()
    main(**kwargs) 
