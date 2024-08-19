
class Inputs():
    def __init__(self):
        self.names = []
        self.inputs = []

    def define_input(self, name, key):
        input = Input(name, key)
        self.inputs.append(input)
        setattr(self, name, False)
    
    def define_impulse(self, name, key):
        input = Input_Impulse(name, key)
        self.inputs.append(input)
        setattr(self, name, False)

    def read(self, keys):
        for input in self.inputs:
            setattr(self, input.name, input.check(keys))
            


class Input():
    def __init__(self, name, key):
        self.name = name
        self.key = key

    def check(self, keys):
        return keys[self.key]


class Input_Impulse(Input):
    def __init__(self, name, key):
        Input.__init__(self, name, key)
        self.ready = True
    
    def check(self, keys):
        pressed = keys[self.key]
        if pressed:
            if self.ready:
                self.ready = False
                return True
            else:
                return False
        else:
            self.ready = True
            return False
        