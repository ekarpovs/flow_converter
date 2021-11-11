class Templates():
  def __init__(self):
    # Predefined transitions
    # TEMPLATE_TRANSITION = ["name", "src", "event", "target", "action", "start-action", "end-action"]
    self._states_transitions = [
      # begin
      [
        self.def_transition(["", "", "next", "", "", "", ""]),
        self.def_transition(["", "", "current", "", "", "", ""]),
      ],
      # regular
      [
        self.def_transition(["", "", "next", "", "", "", ""]),
        self.def_transition(["", "", "current", "", "", "", ""]),
        self.def_transition(["", "", "prev", "", "", "", ""]),
      ],
      # end
      [
        self.def_transition(["", "", "prev", "", "", "", ""]),
      ]
    ]

  @property
  def transitions(self):
    return self._states_transitions

  # Utilites
  @staticmethod
  def _inst_template(keys, values):
    return dict(zip(keys, values))

  def def_fsm(self, values):
    TEMPLATE_FSM = ["info", "context-name", "init-action", "first-state", "states"]    
    return self._inst_template(TEMPLATE_FSM, values)

  def def_state(self, values):
    TEMPLATE_STATE = ["name", "entry-action", "exit-action", "transitions"]
    return self._inst_template(TEMPLATE_STATE, values)

  def def_transition(self, values):
    TEMPLATE_TRANSITION = ["name", "src", "event", "target", "action", "start-action", "end-action"]
    return self._inst_template(TEMPLATE_TRANSITION, values)
