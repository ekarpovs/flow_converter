# Usage:
#   python run.py -w <worksheet full name> -o <output file> [-t no/yes]
# 

import argparse
import json
from typing import Dict, List

from flow_model import FlowModel

from flow_converter import FlowConverter

# Construct the argument parser and parse the arguments
def parseArgs():
  ap = argparse.ArgumentParser(description="flow model")
  ap.add_argument("-w", "--worksheet", required = True,
	help = "the worksheet full name")
  ap.add_argument("-d", "--definition", required = False,
	help = "the definition full name")
  
  args = ap.parse_args()   
  kwargs = dict((k,v) for k,v in vars(args).items() if k!="message_type")
  return kwargs


def load_worksheet(ffn: str) -> List[Dict]:
    # load the worksheet from the path 
    with open(ffn, 'rt') as ws:
      worksheet = json.load(ws)
    return worksheet

def storeFsmDef(ffn, fsm_def) -> None:
  json_object = json.dumps(fsm_def, indent = 2) 
  with open(ffn, "w") as outfile: 
    outfile.write(json_object)
  return


# Main function
def main(**kwargs) -> None: 
  # usage in a client - begin
  ws_ffn = kwargs.get('worksheet')
  ws = load_worksheet(ws_ffn)
  model = FlowModel(ws)

  fc = FlowConverter(model)
  fsm_def = fc.convert()
  # usage in a client - end
  
  def_ffn = kwargs.get('definition', '../data/fsm-def')
  if len(def_ffn) > 0:
    storeFsmDef(def_ffn, fsm_def)
  return

# Entry point
if __name__ == "__main__":
    kwargs = parseArgs()
    main(**kwargs) 
