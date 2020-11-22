# File: vm.py
# Author: Mitchell Angelos
# CMSC 313 - Prof. Potteiger
# Started 10/14/20
# Last edit: 10/14/20

# -----------------------------------------------------------------

####################### IMPORTS ###################################
import shlex

####################### CONSTANTS #################################
# instructions
MOVE = 'mov'
ADD = 'add'
SUB = 'sub'
SYSCALL = 'syscall'
JUMP = 'jmp'
CALL = 'call'

# registers
SYSCALL_ID_REG = 'r1'
DEST_MATH_REG = 'r2'
SRC_MATH_REG = 'r3'
STR_DEST_REG = 'r5'
INPUT_REG = 'r10'

# system call IDs
SCAN = '1'
PRINT = '2'
EXIT = '3'

# keywords
GLOBAL = 'global'
LOCAL = 'lcl'
COMMENT = '#'
FUNC_ENTER = ':'

# file loading
LOAD_FILE = "math.txt"

# misc
EXEC_FUNC = '_start'
END_FUNC = 'end'
NEWLINE = '\n'

####################### VARIABLES #################################

# Data in registers in form of a list, initially empty
regs = { 'r1': '', 'r2': '',
         'r3': '', 'r4': '',
         'r5': '', 'r6': '',
         'r7': '', 'r8': '',
         'r8': '', 'r10': ''}
         

# RIP register to keep track of the current instruction location
rip = []

# STACK for local vars, but in dictionary form
lcl = {}

# Memory for global variables, initialized or uninitialized
# In dictionary form
glbls = {}

# HELPER - A function name to line number dictionary.
# Easy access to line number to find function in code
funcs = {}

########################## FUNCTIONS ####################################

# Function "isValidRegister()" takes a register like "r1" and checks if it
# is a valid register in the Virtual Machine. Only r1-r10 are valid.
# Input - A register as a string
# Output - True if valid register, False otherwise
def isValidRegister(reg):

    return reg in regs.keys()


# Function removeComments() removes comments in split list that contains
# the code.
def removeComments(code):

    for i in range(len(code)):
        code[i] = code[i].split(COMMENT, 1)[0]
        if code[i] != '' and code[i][-1] == ' ':
            code[i] = code[i][:-1]

    for i in range(code.count('')):
        code.remove('')    
        
    
# Function "storeInstructions()" takes a text file with instructions
# and stores it in the RIP register.
# Input - A text file with instructions.
# Output - None
def storeInstructions(lines):

    lineNumber = 0

    for line in lines:
        if line[:3] != LOCAL:
            line = line.lower()
        line = shlex.split(line)
        lineNumber += 1
        classify(line, lineNumber)
                            
                
# Function "classify()" takes a line and classifies it as a
# function enterance, a global or a local
# Input - A line seperated into a list, and a line number
# Output - None
def classify(line, lineNumber):

    if line[0][-1] == FUNC_ENTER:
        funcs[line[0][:-1]] = lineNumber
    elif line[0] == GLOBAL:
        glbls[line[1]] = lineNumber
    elif line[0] == LOCAL:
        lcl[line[1]] = line[2]
        
        
# Function "parseInstruction()" takes the first instruction in the
# RIP register and executes it.
# Input - None.
# Output - None. It will jump to other functions and execute commands.
def parseInstruction(lines, line):

    line = shlex.split(line)
    
    if line[0] == MOVE:
        move(line)
    elif line[0] == SYSCALL:
        systemCall()
    elif line[0] == SUB:
        sub()
    elif line[0] == ADD:
        add()
    elif line[0] == JUMP:
        jump(lines, line)
    elif line[0] == CALL:
        call(lines, line)

# Function 'jump()' jumps to appropriate place in code.
# Input - A list with instructions on where to jump.
# Output - None, line executed jumps to next place
def jump(lines, line):

    rip.clear()
    addRip(lines, funcs[line[1].lower()])

# Function 'call()' calls a function in the code.
# Input - A list with instructions on what to call
# Output - None, calls function specified
def call(lines, line):

    lineNumber = funcs[line[1]]
    while lines[lineNumber] != END_FUNC:
        parseInstruction(lines, lines[lineNumber])
        lineNumber += 1
        
        
# Function 'systemCall()' calls the system based off value in r1.
# Input - No input.
# Output - No output. The system is called and it does what it's
# supposed to do.
# ALL systemCall IDs will be checked in the r1 register.
def systemCall():

    callID = regs.get(SYSCALL_ID_REG)
    if callID == SCAN:
        lcl[regs[INPUT_REG]] = input('')
    elif callID == PRINT:
        print(lcl[regs.get(STR_DEST_REG)])
    elif callID == EXIT:
        sys.exit

# Function "move()" moves
# Input - A list containing the instructions
# Output - None, registers are updated
def move(direcs):
    
    if isValidRegister(direcs[1]):
        if isValidRegister(direcs[2]):
            regs[direcs[1]] = regs[direcs[2]]
        elif direcs[2].isalnum():
            regs[direcs[1]] = direcs[2]
    elif direcs[1] in lcl and isValidRegister(direcs[2]):
        lcl[direcs[1]] = regs.get(direcs[2])
            
    
# Function "add()" adds the source value to its destination.
# Input - A list containing the instructions.
# Output - None, registers are updated
def add():

    regs[DEST_MATH_REG] = str( float(lcl[regs.get(DEST_MATH_REG)]) +
                               float(lcl[regs.get(SRC_MATH_REG)]) )
         
    
# Function "sub()" subtracts source from destination
# Input - A list containing the instructions.
# Output - None, registers are updated
def sub():

    regs[DEST_MATH_REG] = str( float(lcl[regs.get(DEST_MATH_REG)]) -
                               float(lcl[regs.get(SRC_MATH_REG)]) )

    
# Function 'setup()' does some basic actions to start the
# code up with correct values.
# Input - An empty list
# Output - None, lines gets populated with all lines of code
def setup():

    # gets all lines from file into list
    with open(LOAD_FILE) as f:
        lines = f.readlines()
        f.close()
    # removes all lines that are just newlines
    for i in range(lines.count(NEWLINE)):
        lines.remove(NEWLINE)
    # removes all newline characters after each line
    for i in range(len(lines)):
        lines[i] = lines[i][:-1]
    # removes all comment lines and comments in lines
    removeComments(lines)
    return lines


# Program execution
# Stores all code into a list
# Adds to RIP register
# Executes line by line from RIP
def execute(lines):

    storeInstructions(lines)
    addRip(lines, funcs[EXEC_FUNC])
    while len(rip) > 0:
        parseInstruction(lines, rip.pop(0))
        

# Adds lines to the RIP register for execution
def addRip(lines, lineNumber):

    while lines[lineNumber] != END_FUNC:
        rip.append(lines[lineNumber])
        lineNumber += 1
        
        
# Program execution
def main():

    execute(setup())
    

# NOTES
# Like x86, syntax is 'destination source' (omitting the ',')
        
main()
