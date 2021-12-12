from collections import OrderedDict
import graphviz
import pydot
import os
   
os.environ["PATH"] += os.pathsep + "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/graphviz"

class State(object):

    def __init__(self, label):
        self.label = label
        self.transitions = {}
        self.final = False

    def next_state(self, c):
        return self.transitions.get(c, None)

    def accepts(self, w):
        s = self
        for c in w:
            s = s.next_state(c)
            if s is None:
                return False
        return s.final

    def add_transition(self, c, s):
        self.transitions[c] = s

    def add_transition_to_a_new_state(self, c, label):
        s = State(label)
        self.add_transition(c, s)
        return s

    def set_final(self, final):
        self.final = final
        
class MinDict(object):

    def __init__(self, label):
        self.transitions = OrderedDict()

    def last_transition(self):
        k = next(reversed(self.transitions), None)
        if k is not None:
            return k, self.transitions[k]
        else:
            return None

    def minimal_automaton_from_words(words):
        register = MinDict(key_object)
        labels = inf_labels()
        start_state = State(next(labels))
        for word in words:
            last_state, pref_idx = common_prefix(start_state, word)
            if last_state.transitions:
                replace_or_register(last_state, register)
            add_suffix(last_state, word[pref_idx:], labels)
        replace_or_register(start_state, register)
        return start_state, register

    def replace_or_register(state, register):
        last_c, last_child = state.last_transition()
        if last_child.transitions:
            replace_or_register(last_child, register)
        eq_state = register.get(last_child)
        if eq_state is None:
            register.put(last_child)
        else:
            state.add_transition(last_c, eq_state)
    
def draw_automaton(aut):

    g = graphviz.Digraph('Automaton')

    for transition in aut.transitions:
        if transition == aut.last_transition:
            g.attr('node', style='bold')
        if transition == aut.start_state:
            g.node(str(transition), label="-> " + str(transiition))
        else:
            g.node(str(transition))
        g.attr('node', style='solid')

    for x, label, z in aut.transitions:
        g.edge(str(x), str(z), label=" " + label + " ")

    return g

dictionary = ["acker", "alle", "alraune", "as", "aspekt"]
min_dict = MinDict(dictionary)

g = draw_automaton(min_dict)
g.render('graphviz/aut.gv', view = True)
