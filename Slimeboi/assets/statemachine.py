

class StateMachine:
    def __init__(self):
        self.state = None
        self.state_dict = []
        self.trigger_dict = []

    def define_state(self, name, begin, main, end):
        state = State(name, begin, main, end)
        self.state_dict.append(state)
    
    def define_trigger(self, state_from, state_to, condition = lambda: True):
        trigger = Trigger(state_to, condition)

        # Check if the state already exists in our trigger dictionary
        # If so, append the trigger to that state
        exists = False
        for t in self.trigger_dict:
            if t["state_from"] == state_from:
                exists = True
                t["triggers"].append(trigger)
        
        # If the state does not exist, create a listing
        # And append the trigger to that state
        if not exists:
            entry = {"state_from": state_from, "triggers": [trigger]}
            self.trigger_dict.append(entry)

    def process(self):
        if self.state is not None and self.state.main is not None:
            self.state.main()

    def begin(self, newstate):
        state = None
        # Ensure the new state exists
        for entry in self.state_dict:
            if entry.name == newstate:
                state = entry

        # If new state exists, end() current state and begin() new state
        if state is not None:
            if self.state is not None and self.state.end is not None:
                self.state.end()

            self.state = state
            if self.state.begin is not None:
                self.state.begin()
            


    def trigger(self, triggered_state):
        if self.state is None:
            return
        # Check if current state can transition to the triggered state
        # If yes, transition to the new state
        for entry in self.trigger_dict:
            if entry["state_from"] == self.state.name:
                for trigger in entry["triggers"]:
                    if contains(trigger.state_to, triggered_state) and trigger.condition():
                        self.begin(triggered_state)



class State:
    def __init__(self, name, begin, main, end):
        self.name = name    # Name of the state
        # Functions to process
        self.begin = begin  # Process once when state begins
        self.main = main    # Process every frame
        self.end = end      # Process once when state ends

        self.data = None    # Any variable data needed by this state

class Trigger:
    def __init__(self, state_to, condition):
        if not type(state_to) == list:    # Ensure state_to is an array
            state_to = [state_to]
        self.state_to = state_to    # Which state does this trigger lead to?
        self.condition = condition  # What condition needs to be true for this trigger to fire?


# Helper function that should be default in Python lmao
def contains(array, value):
    for item in array:
        if item == value:
            return True
    return False