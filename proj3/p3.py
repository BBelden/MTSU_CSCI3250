# !/usr/bin/env python3.4

# Name:       Ben Belden
# Class ID# :  bpb2v
# Section:    CSCI 3250-001
# Assignment: Project 3
# Turnin ID:  os_p3
# Due:        14:20:00, October 27, 2014
# Purpose:    Implement the virtual machine described in the Machine Specs of the 
#             langdef.txt file that we have used for reference in past assignments.
# Input:      Pre-formatted file.
# Output:     Print to terminal.
#
# File:       p3.py


import sys
import pprint

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in range(0, len(l), n):
        yield l[i:i+n]

opCodes = {"NOP":1,"L":2,"LR":3,"LN":4,"LX":5,"LA":6,"ST":7,"STN":8,"STX":9,"ADD":10,"ADDR":11,"SUB":12,"SUBR":13,"CMP":14,"CMPR":15,"MEMCPY":16,"J":17,"JR":18,"JEQ":19,"JEQR":20,"JNE":21,"JNER":22,"JLT":23,"JLTR":24,"JGT":25,"JGTR":26,"JLE":27,"JLER":28,"JGE":29,"JGER":30,"JSUB":31,"JSUBR":32,"HALT":33,"PREGS":34,"PINT":35}

f = open(sys.argv[1])
loc = int(sys.argv[2])
currLoc = 0
memory = [0 for i in range(16000)]
registers = [0 for i in range(32)]
registers[31] = loc

# load memory
for line in f:
    i = line.find("# ")
    if i >= 0:
        line = line[:i]
    line = line.rstrip()
    if len(line) <= 0:
        continue
    sline = line.split()


    if line[0] == 'T':
        if currLoc != int(sline[1]):
            currLoc = int(sline[1])
        memory[currLoc+loc] = int(sline[2])
        currLoc+=1
        if len(sline) > 3:
            memory[currLoc+loc] = int(sline[3])
            currLoc+=1
            memory[currLoc+loc] = int(sline[4])
            currLoc+=1

    if line[0] == 'R':
        r = int(sline[1])
        memory[loc + r] = memory[loc + r] + loc

    if line[0] == 'Z':
        for x in range (currLoc, currLoc+int(sline[2])):
            memory[x] = 0
        currLoc += int(sline[2])

# for item in memory[loc:currLoc+1]:
#     print item

# execute memory
go = True
while go == True:
    #print(registers[31])

    progCtr = registers[31]
    cmd = memory[progCtr]
    # NOP
    if cmd == 1:
        registers[31]+=3

    # L
    elif cmd == 2:
        registers[memory[progCtr+1]] = memory[progCtr+2]
        registers[31]+=3

    # LR
    elif cmd == 3:
        registers[memory[progCtr+1]] = registers[memory[progCtr+2]]
        registers[31]+=3

    # LN
    elif cmd == 4:
        registers[memory[progCtr+1]] = registers[memory[progCtr+2]]
        registers[31]+=3

    # LX
    elif cmd == 5:
        registers[memory[progCtr+1]] = memory[progCtr+2]
        registers[31]+=3

    # LA
    elif cmd == 6:
        registers[31]+=3

    # ST
    elif cmd == 7:
        memory[progCtr+2] = registers[memory[progCtr+1]]
        registers[31]+=3

    # STN
    elif cmd == 8:
        memory[registers[progCtr+2]] = registers[memory[progCtr+1]] 
        registers[31]+=3

    # STX
    elif cmd == 9:
        registers[31]+=3

    # ADD
    elif cmd == 10:
        registers[memory[progCtr+1]] = registers[memory[progCtr+1]] + memory[progCtr+2]
        registers[31]+=3

    # ADDR
    elif cmd == 11:
        registers[memory[progCtr+1]] = registers[memory[progCtr+1]] + registers[memory[progCtr+2]]
        registers[31]+=3

    # SUB
    elif cmd == 12:
        registers[memory[progCtr+1]] = registers[memory[progCtr+1]] - memory[progCtr+2]
        registers[31]+=3

    # SUBR
    elif cmd == 13:
        registers[memory[progCtr+1]] = registers[memory[progCtr+1]] - registers[memory[progCtr+2]]
        registers[31]+=3

    # CMP
    elif cmd == 14:
        registers[31]+=3

    # CMPR
    elif cmd == 15:
        registers[31]+=3

    # MEMCPY
    elif cmd == 16:
        toAddr = memory[progCtr+2]
        fromAddr = registers[toAddr+1]
        length = registers[toAddr+2]
        x = 0
        while x < length:
            registers[toAddr+x] = registers[fromAddr+x]
            x+=1
        registers[31]+=3

    # J
    elif cmd == 17:
        registers[31] = memory[progCtr+1]

    # JR
    elif cmd == 18:
        registers[31] = registers[progCtr+1]

    # JEQ
    elif cmd == 19:
        if registers[memory[progCtr+1]] == registers[memory[progCtr+2]]:
            registers[31] = memory[progCtr+1]
        else:
            registers[31]+=3

    # JEQR
    #elif cmd == 20:

    # JNE
    elif cmd == 21:
        if registers[memory[progCtr+1]] != registers[memory[progCtr+2]]:
            registers[31] = memory[progCtr+1]
        else:
            registers[31]+=3

    # JNER
    #elif cmd == 22:

    # JLT
    elif cmd == 23:
        if registers[memory[progCtr+1]] < registers[memory[progCtr+2]]:
            registers[31] = memory[progCtr+1]
        else:
            registers[31]+=3

    # JLTR
    #elif cmd == 24:

    # JGT
    elif cmd == 25:
        if registers[memory[progCtr+1]] > registers[memory[progCtr+2]]:
            registers[31] = memory[progCtr+1]
        else:
            registers[31]+=3

    # JGTR
    #elif cmd == 26:

    # JLE
    elif cmd == 27:
        if registers[memory[progCtr+1]] <= registers[memory[progCtr+2]]:
            registers[31] = memory[progCtr+1]
        else:
            registers[31]+=3

    # JLER
    #elif cmd == 28:

    # JGE
    elif cmd == 29:
        if registers[memory[progCtr+1]] >= registers[memory[progCtr+2]]:
            registers[31] = memory[progCtr+1]
        else:
            registers[31]+=3

    # JGER
    #elif cmd == 30:

    # JSUB
    elif cmd == 31:
        registers[memory[progCtr+1]] = registers[31]
        registers[31] = memory[progCtr+2]

    # JSUBR
    elif cmd == 32:
        registers[memory[progCtr+1]] = registers[31]
        registers[31] = memory[progCtr+2]

    # HALT
    elif cmd == 33:
        go = False

    # PREGS
    elif cmd == 34:
        #print("Printing registers:\n")
        x = memory[progCtr+1]
        while x <= memory[progCtr+2]:
            print (registers[x])
            x += 1
        print()
        registers[31]+=3

    # PINT
    elif cmd == 35:
        #print("Printing memory:\n")
        a = memory[progCtr+2]
        b = memory[progCtr+1]
        x = a
        while x < a + b:
            print (memory[x])
            x += 1
        print()
        registers[31]+=3






