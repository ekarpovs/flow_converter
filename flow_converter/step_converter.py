import copy
from .templates import Templates 

class StateType():
  EXEC, STM_BEGIN, STM_END = range(3)
  # EXEC, STM_BEGIN, STM_END, STM_FORINRANGE, STM_WHILE = range(5)

class StateOffset():
  REARWARD, NO, FORWARD = range(-1,2)


class StepConverter():
  def __init__(self, meta):
    self.meta = meta
    return


  def convert(self):
    meta = self.meta
    templates = Templates()
    self.states_transitions = templates.get_transitions()

    def step_name_to_state_def_name(idx, offset=StateOffset.NO):
      step_meta = meta[idx+offset]
      if 'exec' in step_meta:
        step_name = step_meta['exec']
      else:
        step_name = step_meta['stm']
      return "{}-{}".format(idx+offset, step_name.split('.')[1]), step_name


    def converter(idx):
      step_meta = meta[idx]
      def state_type(idx):
        if 'exec' in step_meta:
          return StateType.EXEC
        else:
          stm = step_meta['stm']
          if stm == 'glbstm.begin':
            return StateType.STM_BEGIN
          if stm == 'glbstm.end':
            return StateType.STM_END
      
      state_type = state_type(idx)
      state_transitions = []
      state_transitions = self.states_transitions[state_type]
      state_name, act_name = step_name_to_state_def_name(idx)
      state_entry_action = ''
      state_exit_action = ''
      trans_def = copy.deepcopy(state_transitions)
      for n, tr in enumerate(trans_def):
        tr['name'] = 'tr' + str(idx) + str(n) 
        tr['src'] = state_name
        event_name = trans_def[n]['event'] 
        if event_name == 'next':
          tr['target'], _ = step_name_to_state_def_name(idx, StateOffset.FORWARD)
          if idx > 0 and idx < len(meta)-1:
            # Set an action for regular states only
            tr['action'] = act_name
        elif event_name == 'prev':
          tr['target'], _ = step_name_to_state_def_name(idx, StateOffset.REARWARD)
        else: # 'current'
          tr['target'] = state_name
          if idx > 0 and idx < len(meta)-1:
            # Set an action for regular states only
            tr['action'] = act_name
      return state_name, trans_def, state_entry_action, state_exit_action
    return converter    
