class Templates():
  def __init__(self):
    # Predefined transitions
    # TEMPLATE_TRANSITION = ["name", "src", "event",
    # "target", "action", "start-action", "end-action"]
    self._states_transitions = [
        [
            # 0. begin
            self.transition_def(["", "", "next", "", "", "", ""]),
            self.transition_def(["", "", "current", "", "", "", ""])
        ],
        [
            # 1. regular
            self.transition_def(["", "", "next", "", "", "", ""]),
            self.transition_def(["", "", "current", "", "", "", ""]),
            self.transition_def(["", "", "prev", "", "", "", ""])
        ],
        [
            # 2. end
            self.transition_def(["", "", "prev", "", "", "", ""]),
            self.transition_def(["", "", "current", "", "", "", ""])
        ],
        [
            # 3. if_begin, while_begin, for_begin
            self.transition_def(["", "", "next", "", "", "", ""]),
            self.transition_def(["", "", "current", "", "", "", ""]),
            self.transition_def(["", "", "end_stm", "", "", "", ""]),
            self.transition_def(["", "", "prev", "", "", "", ""])
        ],
        [
            # 4. if_end
            self.transition_def(["", "", "next", "", "", "", ""]),
            self.transition_def(["", "", "begin_stm", "", "", "", ""])
        ],
        [
            # 5. while_end, for_end
            self.transition_def(["", "", "begin_stm", "", "", "", ""])
        ]
    ]

  @property
  def transitions(self):
    return self._states_transitions

    # Utilites
  @staticmethod
  def _inst_template(keys, values):
    return dict(zip(keys, values))

  def fsm_def(self, values):
    TEMPLATE_FSM = ["info", "context-name",
                    "init-action", "first-state", "states"]
    return self._inst_template(TEMPLATE_FSM, values)

  def state_def(self, values):
    TEMPLATE_STATE = ["name", "entry-action", "exit-action", "transitions"]
    return self._inst_template(TEMPLATE_STATE, values)

  def transition_def(self, values):
    TEMPLATE_TRANSITION = ["name", "src", "event", "target",
                           "action", "start-action", "end-action"]
    return self._inst_template(TEMPLATE_TRANSITION, values)
