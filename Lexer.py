from typing import Set, Dict, List

class DFA:
    def __init(self):
        self._alphabet: set()
        self._token: str
        self._initialState: str
        self._currentState: str
        self._finalStates: set()
        self._delta: Dict[str, Dict[str, str]]
        return self

def wordAccepted(dfa: DFA, word):
    state = 0
    length = 0
    maxLen = 0

    while word is not "":
            
        if checkNextStep(dfa, word) == 1:
            state = dfa._delta[dfa._currentState][word[0]]
        else:
            return maxLen

        length = length + 1
        word = word[1:]
        dfa._currentState = state 
        
        if state in dfa._finalStates:
            maxLen = length
   
    return maxLen

def checkNextStep(dfa: DFA, word):

    if dfa._currentState not in dfa._delta.keys() or word[0] not in dfa._delta[dfa._currentState].keys():
        return 0
    return 1

def runlexer(lex, input, output):
    
    dfas = list()
    f = open(input, "r")
    word = ""

    for i in f:
        word = word + i
    f.close()
    
    f = open(lex, "r")
    inputLex = ""

    for i in f:
        inputLex = inputLex + i
    f.close()

    index = 0
    maxLen = 0
    length = 0

    dfaString = inputLex.split("\n\n")

    for i in range(len(dfaString)):
        dfa = DFA()
        if dfaString[i][0] == "\\":
            
            dfa._alphabet = set('\n')
            lines = dfaString[i].splitlines(True)
            dfa._token = lines[1][:-1]
            dfa._initialState = lines[2][:-1]
            dfa._finalStates = set(lines[len(lines) - 1].split(" "))

            lines = lines[3:]
            lines = lines[:-1]
            dfa._delta = {}

            for i in range(0, len(lines) - 1, 2):
                if lines[i][0] not in dfa._delta.keys():
                    dfa._delta[lines[i][0]] = {}
                dfa._delta[lines[i][0]]['\n'] = lines[i][-2]
        
        else:
            lines = dfaString[i].splitlines()
            dfa._alphabet = set(lines[0])
            dfa._token = lines[1]
            dfa._initialState = lines[2]
            dfa._finalStates = set(lines[len(lines) - 1].split(" "))
            lines = lines[3:]
            dfa._delta = {}

            for i in range(len(lines) - 1):
                tr = lines[i].split(",")

                if tr[0] not in dfa._delta.keys():
                    dfa._delta[tr[0]] = {}
                dfa._delta[tr[0]][tr[1][1]] = tr[2]
        
        dfas.append(dfa)
        
    for dfa in dfas:
        dfa._currentState = dfa._initialState
        
    f = open(output, "w")
    
    while word is not "":
        
        for i in range(len(dfas)):
            length = wordAccepted(dfas[i], word)
            
            if length > maxLen:
                index = i
                maxLen = length   
    
        if word[0] is not '\n':
            f.write(dfas[index]._token + " " + word[0:maxLen])
            f.write('\n')
            
        else:
            f.write(dfas[index]._token + '\\n')
            f.write('\n')
            
        word = word[maxLen:]
        maxLen = 0
        
        for i in range(len(dfas)):
            dfas[i]._currentState = dfas[i]._initialState