***Minimal Dictionary Automaton***

The minimal finite state machine programme with the classes State and MinDict is saved in the file **minimal-automaton.py** along with the main part of the programme. There are also a couple of word lists stored in the zip file, in case the user does not have such list available: **english.txt** and **deutsch.txt**. Both lists are utf-8 encoded. Note: the user cannot access files that are out of the directory where the python programme is located.

***Executing the programme: the Welcome menu***

To call the programme, the user has to enter *python3 minimal-automaton.py* in the command line. A welcome menu with two options will then be displayed. If the user enters *1*, they  will have to introduce the name of a file containing a word list. This way, a new automaton from will be created.  In the event that the user had already started the programme in the past, they would be able to load the existing file with the automaton by entering *2*.

The file with the word list contains words separated line by line with new lines.

***Main part***

Once the automaton has been generated, the user will see a main menu consisting of the following options:

* (1) Checks whether a word is in the lexicon.
* (2) Draws an automaton using the module GraphViz.
* (3) Displays all the words that are part of the automaton. In the class MinDict() there is a method **recursive_search**, which looks for the words recursively.
* (4) Saves the automaton that was just generated so that the user can load it next time you start a programme when they choose the option *2* in the ***Welcome menu***. The file is saved as a pickle file **minimal_dictionary.pkl**.
* (X) Exits the programme. If the user wishes to terminate the programme, they can simply enter *X* or *x*.

If the option introduced by the user is not available, a message will be shown prompting them to enter a valid choice.

***Possible error messages***

* FileNotFoundError: if the file name entered is not found. The programme will be automatically finished.
* Option not available error: if the option entered by the user either in the ***Welcome menu*** or ***Main menu*** is not valid, they will be prompted to introduce a valid option.

***Implemented extensions***

* Save and load
* Get language of the automaton
* Draw automaton with third-party module GraphViz