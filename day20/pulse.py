import sys
from queue import Queue
from functools import reduce

workflow = Queue()
modules = {}

class Signal(object):
    def __init__(self, src, tar, s):
        self.source = src
        self.target = tar
        self.signal = s

# Parent class of Module. Not generating any pulse
class Module(object):
    def __init__(self):
        self.current = False # the current pulse
        self.inputs = {}     # the input and its pulse remembered in the module
        self.outputs = []    # the dest modules

    def process(self, new_input):
        return 0,False

    def original_state(self):
        return True

# Module of Broadcaster, simply send input pulse to all outputs
class Broadcaster(Module):
    def process(self, new_input):
        self.current = new_input.signal
        for dest in self.outputs:
            workflow.put(Signal(self, dest, new_input.signal))
        return len(self.outputs), new_input.signal

    def original_state(self):
        return True

# Module Flip Flop 
class Flipflop(Module):
    def process(self, new_input):
        self.inputs[new_input.source] = new_input.signal
        # if it's low, toggle the current pulse and send to all outputs
        if not new_input.signal:
            self.current = not self.current
            for dest in self.outputs:
                workflow.put(Signal(self, dest, self.current))
            return len(self.outputs), self.current
        return 0, self.current

    def original_state(self):
        # if itself is low, it's now back to original
        return not self.current

# Module Conjuction
class Conjuction(Module):
    def process(self, new_input):
        self.inputs[new_input.source] = new_input.signal

        # the current state is high if all inputs are high
        self.current = not reduce(lambda x, y: x and y, self.inputs.values())
        for dest in self.outputs:
            workflow.put(Signal(self, dest, self.current))
        return len(self.outputs), self.current

    def original_state(self):
        # if all inputs are remembered as low, it's now back to original
        return not reduce(lambda x, y: x or y, self.inputs.values())

def construct_modules(filename):
    output_map = {}
    with open(filename, 'r') as file:
        for line in file:
            str_module = line.split('->')[0].strip()
            str_outputs = [x.strip() for x in line.split('->')[1].strip().split(',')]

            # create Modules objects for left operand.
            # put labels of the right operand to a map, as those modules may not be created yet
            if str_module == 'broadcaster':
                modules['broadcaster'] = Broadcaster()
                output_map['broadcaster'] = str_outputs
            elif str_module[0] == '%':
                modules[str_module[1:]] = Flipflop()
                output_map[str_module[1:]] = str_outputs
            elif str_module[0] == '&':
                modules[str_module[1:]] = Conjuction()
                output_map[str_module[1:]] = str_outputs

    for m, outputs in output_map.items():
        for o in outputs:
            # Create a Module for those right-only operand. They don't have function to send pulse
            if o not in modules:
                modules[o] = Module()
            # Now all modules are created. Put input into output module, and put output into input module
            modules[m].outputs.append(modules[o])
            modules[o].inputs[modules[m]] = False

def one_push():
    low = 1 # always start with low button push
    high = 0
    workflow.put(Signal(None, modules['broadcaster'], False))

    # process signals continuously until the queue is clean
    while (not workflow.empty()):
        s = workflow.get()
        n,lh = s.target.process(s)
        if lh:
            high = high + n
        else:
            low = low + n

    # if all modules are back to the original state, the loop is over and we got the total pulse number in a loop
    x = True
    for v in modules.values():
        x = x and v.original_state()

    return (low, high, x)


def main(filename):
    construct_modules(filename)

    loops = []
    loop_iter = 0
    loopl = 0
    looph = 0
    while True:
        l, h, loop = one_push()
        loops.append((l, h))
        loop_iter = loop_iter + 1
        loopl = loopl + l
        looph = looph + h
        if loop:
            break

    # we got the pulse number for one loop. Now calculate for 1000 pushes
    loop_number = int(1000 / loop_iter)
    resultl = loop_number * loopl
    resulth = loop_number * looph
    for i in range(loop % loop_iter):
        resultl + loops[i][0]
        resulth + loops[i][1]

    print(resultl * resulth)

if __name__=='__main__':
    if len(sys.argv) != 2:
        print("Usage: pulse.py FILENAME\n")
        sys.exit(1)
    main(sys.argv[1])
