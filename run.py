# Usage:
#   python run.py -w <worksheet full name> -o <output file> [-t no/yes]
# 

import argparse
import json

from flow_model import FlowModel

from flow_converter import FlowConverter

# Construct the argument parser and parse the arguments
def parseArgs():
  ap = argparse.ArgumentParser(description="flow model")
  ap.add_argument("-d", "--dir", required = True,
	help = "path to the directory with the worksheet")
  ap.add_argument("-f", "--file", required = True,
	help = "the worksheet file name")
  ap.add_argument("-o", "--output", required = True,
	help = "full path to the output file")
  ap.add_argument("-t", "--trace", required = False,
  default="no", 
	help = "print output")
  
  args = ap.parse_args()   
  kwargs = dict((k,v) for k,v in vars(args).items() if k!="message_type")
  return kwargs


def storeFsmDef(out_path, fsm_def):
  ffn = "{}/fsm-def.json".format(out_path)
  json_object = json.dumps(fsm_def, indent = 2) 
  with open(ffn, "w") as outfile: 
    outfile.write(json_object)
  return


# Main function
def main(**kwargs): 
  # usage in a client - begin
  model = FlowModel(kwargs.get('dir'))
  model.load_worksheet(kwargs.get('file'))

  fc = FlowConverter(model)
  fsm_def = fc.convert()
  # usage in a client - end
  
  output_path = kwargs.get('output', '../data/fsm-def')
  if kwargs.get('trace', 'no') == 'yes':
    storeFsmDef(output_path, fsm_def)

# Entry point
if __name__ == "__main__":
    kwargs = parseArgs()
    main(**kwargs) 
