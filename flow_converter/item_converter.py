import copy
from typing import Tuple

from flow_model import FlowItemModel
from flow_model.flowitemtype import FlowItemType

from .templates import Templates 

class StateType():
  EXEC, STM_BEGIN, STM_END = range(3)
  # EXEC, STM_BEGIN, STM_END, STM_FORINRANGE, STM_WHILE = range(5)

class StateOffset():
  REARWARD, NO, FORWARD = range(-1,2)


class ItemConverter(): 
  def __init__(self, idx: int, item: FlowItemModel) ->None:
    self._idx = idx
    self._item = item
    return

  @property
  def _item_name_to_state_def_name(self) ->str:
    return f'{self._item.name.split(".")[1]}'

  @property
  def _item_name_to_current_state_def_name(self) ->str:
    return f'{self._idx}-{self._item_name_to_state_def_name}'

  @property
  def _item_name_to_next_state_def_name(self) ->str:
    return f'{self._idx+1}-{self._item_name_to_state_def_name}'

  @property
  def _item_name_to_prev_state_def_name(self) ->str:
    return f'{self._idx-1}-{self._item_name_to_state_def_name}'

  @property
  def regular_state(self):
    return self._item.itype == FlowItemType.EXEC

  def convert_model_item(self):
    templates = Templates()
    transitions = templates.transitions
    transitions_def = transitions[self._item.itype]    
    state_name = self._item_name_to_current_state_def_name
    act_name = self._item.name
    state_entry_action = ''
    state_exit_action = ''
    trans_def = copy.deepcopy(transitions_def)
    for n, tr in enumerate(trans_def):
      tr['name'] = f'tr{self._idx}{n}' 
      tr['src'] = state_name
      event_name = trans_def[n]['event'] 
      if event_name == 'next':
        tr['target'] = self._item_name_to_next_state_def_name
        if self.regular_state:
          # Set an action for regular states only
          tr['action'] = act_name
      elif event_name == 'prev':
        tr['target'] = self._item_name_to_prev_state_def_name
      else: # 'current'
        tr['target'] = state_name
        if self.regular_state:
          # Set an action for regular states only
          tr['action'] = act_name
    return state_name, trans_def, state_entry_action, state_exit_action
