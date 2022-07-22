import copy
from typing import List

from flow_model import FlowItemModel

from .templates import Templates


class ItemConverter():
  def __init__(self, idx: int, items: List[FlowItemModel]) -> None:
    self._idx = idx
    self._items = items
    self._templates = Templates()
    return

  def _get_item_name_to_current_state_def_name(self) -> str:
    return f'{self._idx}-{self._items[self._idx].name.split(".")[1]}'

  def _get_item_name_to_next_state_def_name(self) -> str:
    return f'{self._idx + 1}-{self._items[self._idx + 1].name.split(".")[1]}'

  def _get_item_name_to_prev_state_def_name(self) -> str:
    return f'{self._idx - 1}-{self._items[self._idx - 1].name.split(".")[1]}'

  def _get_item_name_to_next_after_end_state_def_name(self) -> str:
    # find if_end index
    for i, item in enumerate(self._items):
      if (i > self._idx) and self._if_statements_end(self._items[i].name):
        break
    return f'{i + 1}-{self._items[i + 1].name.split(".")[1]}'

  def _get_item_name_to_prev_begin_state_def_name(self) -> str:
    for i, item in enumerate(self._items):
      if (i < self._idx) and self._if_statements_begin(self._items[i].name):
        break
    return f'{i}-{self._items[i].name.split(".")[1]}'

  def _if_statements_end(name: str) -> bool:
    stm_end = ['glbstm.if_end', 'glbstm.while_end', 'glbstm.for_end']
    return name in stm_end

  def _if_statements_begin(name: str) -> bool:
    stm_begin = ['glbstm.if_begin', 'glbstm.while_begin', 'glbstm.for_begin']
    return name in stm_begin

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
    state_name = self._get_item_name_to_current_state_def_name()
    act_name = self._items[self._idx].name
    state_entry_action = ''
    state_exit_action = ''
    trans_def = copy.deepcopy(transitions_def)
    for n, tr in enumerate(trans_def):
      tr['name'] = f'tr{self._idx}{n}'
      tr['src'] = state_name
      event_name = trans_def[n]['event']
      if event_name == 'next':
        tr['target'] = self._get_item_name_to_next_state_def_name()
        tr['action'] = act_name
      elif event_name == 'end_stm':
        tr['target'] = self._get_item_name_to_next_after_end_state_def_name()
      elif event_name == 'begin_stm':
        tr['target'] = self._get_item_name_to_prev_begin_state_def_name()
      elif event_name == 'prev':
        tr['target'] = self._get_item_name_to_prev_state_def_name()
      elif event_name == 'begin_stm':
        tr['target'] = self._get_item_name_to_prev_begin_state_def_name()
      else:
        # 'current'
        tr['target'] = state_name
        tr['action'] = act_name
    # TEMPLATE_STATE = ["name", "entry-action", "exit-action", "transitions"]
    state_def = self._templates.state_def([state_name,
                                          state_entry_action,
                                          state_exit_action, trans_def])
    return state_name, state_def
