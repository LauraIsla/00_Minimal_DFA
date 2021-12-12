from collections import OrderedDict
import graphviz
import pickle
import os.path
import sys
from argparse import ArgumentParser

def create_alphabet(filename):
    path = os.path.abspath(filename)
    lexicon = []
    try:
        with open(path, "r", encoding = "utf-8") as text:
            words = [word for word in text.read().splitlines()]
            for line in words:
                lexicon.append(line)
            return(sorted(lexicon))
    except FileNotFoundError:
        print("File not found. See you later!")
        sys.exit(1)


class State():
    
    next_index = 0
    
    def __init__(self,is_final,is_in_register,transitions):
        self.is_final = is_final
        self.index = State.next_index
        State.next_index += 1
        self.is_in_register = False
        self.transitions = transitions
        
    def unique_repr(self):
        return ("F" if self.is_final else "N") \
        + "".join([str(label) + str(target.index) for label, target in self.transitions.items()])
    
    def add_transition(self,label,target_state):
        self.transitions[label] = target_state
        
    def transition(self,label):
        if label in self.transitions.keys():
            return self.transitions[label]
        
    def delete_transition(self,label):
        del self.transitions[label]
        
    def get_last_child(self):
        for state in reversed(self.transitions.values()):
            return state
    
    def get_last_label(self):
        for label in reversed(self.transitions.keys()):
            return label

    def has_children(self):
        if len(self.transitions) == 0:
            return False
        else:
            return True
    
    def final(self):
        self.is_final = True

class MinDict:

    def __init__(self, lexicon):
        self.lexicon = list(lexicon)
        self.register = []
        self.final_states = []
        self.all_states = []
        self.language = []
        self.start_state = State(False, False, OrderedDict())
        self.all_states.append(self.start_state)
        self.alphabet = sorted({char for word in self.lexicon for char in word})

        for word in self.lexicon:
            commonPrefix, lastState = self.common_prefix(word)
            longestCommonPrefix = word[:commonPrefix]
            currentSuffix = word[len(longestCommonPrefix):]
            if lastState.has_children():
                self.replace_or_register(lastState)
            self.add_suffix(lastState, currentSuffix)

        self.replace_or_register(self.start_state)

    def add_suffix(self, state, suffix):
        for char in suffix:
            target = State(False, False, OrderedDict())
            state.add_transition(char, target)
            self.all_states.append(target)
            state = target
            if char == suffix[-1]:
                state.final()
                self.final_states.append(state)

                
    def common_prefix(self, word):
        i = 0
        current_state = self.start_state
        for char in word:
            if current_state.transition(char):
                current_state = current_state.transition(char)
                i += 1
            else:
                return i, current_state

    def replace_or_register(self, state):
        child = state.get_last_child()
        eq_list = []
        if child.has_children():
            self.replace_or_register(child)
        eq_state = None
        for q in self.register:
            if q.unique_repr() == child.unique_repr():
                eq_list.append(child)
                eq_state = q
        if eq_state != None:
            self.all_states = [state for state in self.all_states if state not in eq_list]
            label = state.get_last_label()
            state.add_transition(label, eq_state)
        else:
            self.move_to_register(child)

    def move_to_register(self, state):
        state.is_in_register = True
        self.register.append(state)

    def delta_dict(self):
        delta = dict()
        for state in self.all_states:
            for char in self.alphabet:
                if state.transition(char):
                    target = state.transition(char)
                    delta.update({(state, char): target})
        return delta

    def recursive_search(self, state, memory=[]):
        if state.is_final:
            self.language.append("".join(memory))
    
        for label, next_state in state.transitions.items():
            memory.append(label)
            self.recursive_search(next_state)
            memory.pop()
        
        return self.language
    
    def get_language(self):
        return self.recursive_search(self.start_state)

    def get_register(self): 
        return sorted([state.index for state in self.register])

    def get_final_states(self):
        return sorted([state.index for state in self.final_states])
    
    def get_all_states(self):
        return sorted([state.index for state in self.all_states])

    def get_delta(self):
        return {(start.index, label, target.index) for (start, label), target in self.delta_dict().items()}

    def draw_automaton(self):
        draw = graphviz.Digraph('Minimal Dictionary Automaton')
        draw.graph_attr['rankdir'] = 'LR'
        all_states = self.get_all_states()
        start_state = all_states[0]
        for state in all_states:
            if state in self.get_final_states():
                draw.attr('node',style='bold')
            if state == start_state:
                draw.node(str(state), label="-> " + str(state))
            else:
                draw.node(str(state))
            draw.attr('node',style='solid')
    
        for start, label, target in self.get_delta():
            draw.edge(str(start), str(target), label=" " + label+ " ")
    
        return draw.render('Automaton.gv', view=True)

    

def main():

    parser = ArgumentParser(description = "Minimal Dictionary Automaton")
    parser.add_argument("-wl", "--word_list", type=str,default="wordlist.txt", help="Path to the sorted word list")
    parser.add_argument("-f", "--file", type = str, default = "minimal_dictionary.pkl", help = "File name for saved automaton")

    args = parser.parse_args()

    construction = True
    while construction:

        print("***Welcome***\nWhat would you like to do today?\n(1) Create new automaton from text file. Note: you need to know the file name.\n(2) Load an existing automaton from a file")
        answer = input("Enter a number >> ")

        if answer == "1":
            word_list_filename = input("Please enter the file name to create the new automaton >>> ")
            word_list = create_alphabet(word_list_filename)
            automaton = MinDict(word_list)
            print("Congratulations, a new automaton was created.")
            construction = False
                
        elif answer == "2":
            try:
                with open(args.file, "rb") as loaded:
                    automaton = pickle.load(loaded)
                print("Congratulations, the automaton was loaded.")
                construction = False
            except FileNotFoundError:
                print("There is no file with a saved automaton. Please enter a file name to create the new automaton.")

        else:
            print("Sorry, that option is not available. Please enter a valid option.")


    run = True
    while run:

        print("What would you like to do next?\n(1) Check whether a word is in the lexicon\n(2) Draw an automaton\n" \
              "(3) Obtain the language of the automaton\n(4) Save the automaton\n(X) Exit programme")
        option = input("Please choose one of the options above >> ")

        if option == "1":
            programme = True
            while programme:
                input_word = input("If you want to exit this programme, just press enter.\nPlease enter a word >> ")
                if input_word == '':
                    programme = False
                elif input_word in automaton.get_language(): 
                    print(input_word, "is in the lexicon.")
                else:
                    print(input_word, "is NOT in the lexicon.")

        elif option == "2":
            print(automaton.draw_automaton())

        elif option == "3":
            print(automaton.get_language())
            automaton.language.clear()

        elif option == "4":
            with open(args.file, "wb") as saved:
                pickle.dump(automaton, saved, pickle.HIGHEST_PROTOCOL)
            print("The automaton was saved.")

        elif option == "X" or option == "x":
            run = False
            print("See you later!")

        else:
            print("Please enter a valid option.")

if __name__ == '__main__':
    main()
          
