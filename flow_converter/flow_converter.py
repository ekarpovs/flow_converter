from flow_model import FlowModel

from .templates import Templates
from .item_converter import ItemConverter


class FlowConverter():
  def __init__(self, model: FlowModel) -> None:
    self._model = model
    self.templates = Templates()

  def model_to_fsm_def(self):
    states_def = []
    first_state_name = None
    for i, item in enumerate(self._model.items):
        # state_entry_action = ""
        # state_exit_action = ""
      item_converter = ItemConverter(i, self._model.items)
      state_name, state_def = item_converter.convert_model_item()
      if item.name == 'glbstm.begin':
        first_state_name = state_name
        # TEMPLATE_STATE=["name", "entry-action", "exit-action", "transitions"]
      states_def.append(state_def)
    # TEMPLATE_FSM=["info", "context-name",
    #       "init-action", "first-state", "states"]
    fsm_def = \
        self.templates.fsm_def(['', '', '', first_state_name, states_def])
    return fsm_def

  def convert(self):
    fsm_def = self.model_to_fsm_def()
    return fsm_def
