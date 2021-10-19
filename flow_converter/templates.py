class Templates():
  def __init__(self):
    # Predefined transitions
    # TEMPLATE_TRANSITION = ["name", "src", "event", "target", "action", "start-action", "end-action"]
    self.states_transitions = [
      # exec
      [
        self.def_transition(["", "", "next", "", "", "", ""]),
        self.def_transition(["", "", "current", "", "", "", ""]),
        self.def_transition(["", "", "prev", "", "", "", ""]),
      ],
      # begin
      [
        self.def_transition(["", "", "next", "", "", "", ""]),
      ],
      # end
      [
        self.def_transition(["", "", "prev", "", "", "", ""]),
      ]
    ]

  def get_transitions(self):
    return self.states_transitions

  # Utilites
  @staticmethod
  def inst_template(keys, values):
    return dict(zip(keys, values))

  def def_fsm(self, values):
    TEMPLATE_FSM = ["info", "context-name", "init-action", "first-state", "states"]    
    return self.inst_template(TEMPLATE_FSM, values)

  def def_state(self, values):
    TEMPLATE_STATE = ["name", "entry-action", "exit-action", "transitions"]
    return self.inst_template(TEMPLATE_STATE, values)

  def def_transition(self, values):
    TEMPLATE_TRANSITION = ["name", "src", "event", "target", "action", "start-action", "end-action"]
    return self.inst_template(TEMPLATE_TRANSITION, values)
