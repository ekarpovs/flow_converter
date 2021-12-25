import copy
from typing import List

from flow_model import FlowItemModel
from flow_model.flowitemtype import FlowItemType

from .templates import Templates 

class ItemConverter(): 
  def __init__(self, idx: int, items: List[FlowItemModel]) ->None:
    self._idx = idx
    self._items = items
    self._templates = Templates()
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

  @property
  def _item_name_to_next_after_end_state_def_name(self) ->str:
    # find if_end index
    for i, item in enumerate(self._items):
      if i > self._idx and (self._items[i].name == 'glbstm.if_end' or 
        self._items[i].name == 'glbstm.while_end' or
        self._items[i].name == 'glbstm.for_end'):
        break
    return f'{i+1}-{self._items[i+1].name.split(".")[1]}'

  @property
  def _item_name_to_prev_begin_state_def_name(self) ->str:
    for i, item in enumerate(self._items):
      if i < self._idx and (self._items[i].name == 'glbstm.if_begin' or
        self._items[i].name == 'glbstm.while_begin' or
        self._items[i].name == 'glbstm.for_begin'):
        break
    return f'{i}-{self._items[i].name.split(".")[1]}'

  def _get_state_transitions_def(self) -> int:
    tr_idxs = {
      'glbstm.begin': 0,
      'glbstm.end': 2,
      'glbstm.if_begin': 3,
      'glbstm.if_end': 4,
      'glbstm.while_begin': 3,
      'glbstm.while_end': 5,
      'glbstm.for_begin': 3,
      'glbstm.for_end': 5
    }
    tr_idx = tr_idxs.get(self._items[self._idx].name, 1)
    return self._templates.transitions[tr_idx]

  def convert_model_item(self):
    transitions_def = self._get_state_transitions_def() 
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
      elif event_name == 'next_end':
        tr['target'] = self._item_name_to_next_after_end_state_def_name
      elif event_name == 'next_begin':
        tr['target'] = self._item_name_to_prev_begin_state_def_name
      elif event_name == 'prev':
        tr['target'] = self._item_name_to_prev_state_def_name
      elif event_name == 'prev_begin':
        tr['target'] = self._item_name_to_prev_begin_state_def_name
      else: # 'current'
        tr['target'] = state_name
        tr['action'] = act_name
    # TEMPLATE_STATE = ["name", "entry-action", "exit-action", "transitions"]
    state_def = self._templates.state_def([state_name, state_entry_action, state_exit_action, trans_def])
    return state_name, state_def
    # return state_name, trans_def, state_entry_action, state_exit_action
