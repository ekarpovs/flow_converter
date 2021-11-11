import copy
from typing import List

from flow_model import FlowItemModel
from flow_model.flowitemtype import FlowItemType

from .templates import Templates 

class ItemConverter(): 
  def __init__(self, idx: int, items: List[FlowItemModel]) ->None:
    self._idx = idx
    self._items = items
    return

  @property
  def _item_name_to_current_state_def_name(self) ->str:
    return f'{self._idx}-{self._items[self._idx].name.split(".")[1]}'

  @property
  def _item_name_to_next_state_def_name(self) ->str:
    return f'{self._idx+1}-{self._items[self._idx+1].name.split(".")[1]}'

  @property
  def _item_name_to_prev_state_def_name(self) ->str:
    return f'{self._idx-1}-{self._items[self._idx-1].name.split(".")[1]}'

  def _get_state_template_idx(self):
    if self._idx > 0 and self._idx < len(self._items)-1:
      return 1
    if self._idx == len(self._items)-1:
      return 2
    return 0

  def convert_model_item(self):
    templates = Templates()
    transitions = templates.transitions
    tr_idx = self._get_state_template_idx()
    transitions_def = transitions[tr_idx]    
    state_name = self._item_name_to_current_state_def_name
    act_name = self._items[self._idx].name
    state_entry_action = ''
    state_exit_action = ''
    trans_def = copy.deepcopy(transitions_def)
    for n, tr in enumerate(trans_def):
      tr['name'] = f'tr{self._idx}{n}' 
      tr['src'] = state_name
      event_name = trans_def[n]['event'] 
      if event_name == 'next':
        tr['target'] = self._item_name_to_next_state_def_name
        tr['action'] = act_name
      elif event_name == 'prev':
        tr['target'] = self._item_name_to_prev_state_def_name
      else: # 'current'
        tr['target'] = state_name
        tr['action'] = act_name
    return state_name, trans_def, state_entry_action, state_exit_action
