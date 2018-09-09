#!/usr/bin/env python3.4

# Name:       Ben Belden
# Class ID# :  bpb2v
# Section:    CSCI 3250-001
# Assignment: Project 4
# Turnin ID:  os_p4
# Due:        14:20:00, November 5, 2014
# Purpose:    Enhance p3 such that your machine can run 2 processes at once, using multiprogramming.
# Input:      Pre-formatted files.
# Output:     Print to terminal.
#
# File:       p4.py


import sys
import copy

memory = [0 for i in range(16000)]
registers = [0 for i in range(32)]
waiting = [0 for i in range(32)]
temp = [0 for i in range(32)]
f = open(sys.argv[1])
loc = int(sys.argv[2])
f2 = open(sys.argv[3])
loc2 = int(sys.argv[4])
currLoc = 0
registers[31] = loc
waiting[31] = loc2
#print (loc, loc2)

# load memory
for line in f:
    i = line.find("# ")
    if i >= 0:
        line = line[:i]
    line = line.rstrip()
    if len(line) <= 0:
        continue
    sline = line.split()

    if sline[0] == 'T':
        if currLoc != int(sline[1]):
            currLoc = int(sline[1])
        memory[currLoc+loc] = int(sline[2])
        currLoc+=1
        if len(sline) > 3:
            memory[currLoc+loc] = int(sline[3])
            currLoc+=1
            memory[currLoc+loc] = int(sline[4])
            currLoc+=1
    if sline[0] == 'R':
        r = int(sline[1])
        memory[loc + r] = memory[loc + r] + loc
    if sline[0] == 'Z':
        for x in range (currLoc, currLoc+int(sline[2])):
            memory[x] = 0
        currLoc += int(sline[2])

#y=loc
#for x in memory[loc:currLoc+loc]:
#    #print (y, ": ", x)
#    y+=1

currLoc = 0
for line in f2:
    i = line.find("# ")
    if i >= 0:
        line = line[:i]
    line = line.rstrip()
    if len(line) <= 0:
        continue
    sline = line.split()

    if sline[0] == 'T':
        if currLoc != int(sline[1]):
            currLoc = int(sline[1])
        memory[currLoc+loc2] = int(sline[2])
        currLoc+=1
        if len(sline) > 3:
            memory[currLoc+loc2] = int(sline[3])
            currLoc+=1
            memory[currLoc+loc2] = int(sline[4])
            currLoc+=1

    if sline[0] == 'R':
        r = int(sline[1])
        memory[loc2 + r] = memory[loc2 + r] + loc2

    if sline[0] == 'Z':
        for x in range (currLoc, currLoc+int(sline[2])):
            memory[x] = 0
        currLoc += int(sline[2])

#y=loc2
#for x in memory[loc2:currLoc+loc]:
#    #print (y, ": ", x)
#    y+=1

#print ("\nexecute\n")

# execute memory
go1 = True
go2 = True
op = 1
while go1 == True or go2 == True:
    #print("progCtr:",registers[31])
    progCtr = registers[31]
    cmd = memory[progCtr]
    op1 = memory[progCtr+1]
    op2 = memory[progCtr+2]
    cc = registers[30]
    index = registers[29]

    # NOP
    if cmd == 1:
        #print ("NOP: "cmd,op1,op2,"\nadvance program counter","\n")
        registers[31]+=3

    # L
    elif cmd == 2:
        #print ("L:",cmd,op1,op2,"\nload register",op1," with loc",progCtr+2," value",op2,"\n")
        registers[op1] = op2
        registers[31]+=3

    # LR
    elif cmd == 3:
        #print ("LR:",cmd,op1,op2,"\nload register",op2," value",registers[op2]," into register",op1,"\n")
        registers[op1] = registers[op2]
        registers[31]+=3

    # LN
    elif cmd == 4:
        #print ("LN:",cmd,op1,op2,"\nload into register",op1,"the word at address",registers[op2],"with value",memory[registers[op2]],"\n")
        registers[op1] = memory[registers[op2]]
        registers[31]+=3

    # LX
    elif cmd == 5:
        #print ("LX:",cmd,op1,op2,"\nload into register",op1,"the word at address",op2,"+",index,"with value",memory[op2 + index],"\n")
        registers[op1] = memory[op2 + index]
        registers[31]+=3

    # LA
    elif cmd == 6:
        #print ("LA:",cmd,op1,op2,"\nload register",op1,"with addr",op2, "that has value:",op2,"\n")
        registers[op1] = op2
        registers[31]+=3

    # ST
    elif cmd == 7:
        #print("ST:",cmd,op1,op2,"\nstore register", op1,"that has value",registers[op1],"into memory location",op2,"\n")
        memory[op2] = registers[op1]
        registers[31]+=3

    # STN
    elif cmd == 8:
        #print ("STN:",cmd,op1,op2,"\nstore register",op1," value", registers[op1],"into address",registers[progCtr+2],"\n")
        memory[registers[progCtr+2]] = registers[op1] 
        registers[31]+=3

    # STX
    elif cmd == 9:
        #print ("STX:",cmd,op1,op2,"\nload into location",op2,"+",index,"register",op1,"value",registers[op1],"\n")
        memory[op2 + index] = registers[op1]
        registers[31]+=3

    # ADD
    elif cmd == 10:
        #print ("ADD:",cmd,op1,op2,"\nadd",memory[op2],"to",registers[op1],"in register",op1,"\n")
        registers[op1] = registers[op1] + memory[op2]
        registers[31]+=3

    # ADDR
    elif cmd == 11:
        #print ("ADDR:",cmd,op1,op2,"\nadd",registers[op2],"to",registers[op1],"in register",op1,"\n")
        registers[op1] = registers[op1] + registers[op2]
        registers[31]+=3

    # SUB
    elif cmd == 12:
        #print ("SUBR:",cmd,op1,op2,"\nsubtract",memory[op2],"from",registers[op1],"in register",op1,"\n")
        registers[op1] = registers[op1] - memory[op2]
        registers[31]+=3

    # SUBR
    elif cmd == 13:
        #print ("SUBR:",cmd,op1,op2,"\nsubtract",registers[op2],"from",registers[op1],"in register",op1,"\n")
        registers[op1] = registers[op1] - registers[op2]
        registers[31]+=3

    # CMP
    elif cmd == 14:
        #print ("CMP:",cmd,op1,op2,"\ncompare",registers[op1],"-",memory[op2],"with 0\n")
        if registers[op1] - memory[op2] > 0:
            cc = 1
        if registers[op1] - memory[op2] == 0:
            cc = 0
        if registers[op1] - memory[op2] < 0:
            cc = -1
        registers[31]+=3

    # CMPR
    elif cmd == 15:
        #print ("CMPR:",cmd,op1,op2,"\ncompare",registers[op1],"-",registers[op2],"with 0\n")
        if registers[op1] - registers[op2] > 0:
            cc = 1
        if registers[op1] - registers[op2] == 0:
            cc = 0
        if registers[op1] - registers[op2] < 0:
            cc = -1
        registers[31]+=3

    # MEMCPY
    elif cmd == 16:
        r1 = op2
        r2 = r1+1
        r3 = r1+2
        #print ("MEMCPY:",cmd,op1,op2,"\nr1:",r1,",r2:",r2,",r3",r3,"\n",registers[r1],registers[r2],registers[r3],'\n')
        toAddr = registers[r1]
        fromAddr = registers[r2]
        length = registers[r3]
        x = 0
        while x < length:
            memory[toAddr+x] = memory[fromAddr+x]
            x+=1
        registers[31]+=3

    # J
    elif cmd == 17:
        #print ("J:",cmd,op1,op2,"\n")
        registers[31] = op2

    # JR
    elif cmd == 18:
        #print ("JR:",cmd,op1,op2,"\n")
        registers[31] = memory[registers[progCtr+2]]

    # JEQ
    elif cmd == 19:
        #print ("JEQ:",cmd,op1,op2,"\n")
        if cc == 0:
            registers[31] = op2
        else:
            registers[31]+=3

    # JEQR
    elif cmd == 20:
        #print ("JEQR:",cmd,op1,op2,"\n")
        if cc == 0:
            registers[31] = memory[registers[progCtr+2]]
        else:
            registers[31]+=3

    # JNE
    elif cmd == 21:
        #print ("JNE:",cmd,op1,op2,"\n")
        if cc != 0:
            registers[31] = op2
        else:
            registers[31]+=3

    # JNER
    elif cmd == 22:
        #print ("JNER:",cmd,op1,op2,"\n")
        if cc != 0:
            registers[31] = memory[registers[progCtr+2]]
        else:
            registers[31]+=3

    # JLT
    elif cmd == 23:
        #print ("JLT:",cmd,op1,op2,"\n")
        if cc == -1:
            registers[31] = op2
        else:
            registers[31]+=3

    # JLTR
    elif cmd == 24:
        #print ("JLTR:",cmd,op1,op2,"\n")
        if cc == -1:
            registers[31] = memory[registers[progCtr+2]]
        else:
            registers[31]+=3

    # JGT
    elif cmd == 25:
        #print ("JGT:",cmd,op1,op2,"\n")
        if cc == 1:
            registers[31] = op2
        else:
            registers[31]+=3

    # JGTR
    elif cmd == 26:
        #print ("JGTR:",cmd,op1,op2,"\n")
        if cc == 1:
            registers[31] = memory[registers[progCtr+2]]
        else:
            registers[31]+=3

    # JLE
    elif cmd == 27:
        #print ("JLE:",cmd,op1,op2,"\n")
        if cc != 1:
            registers[31] = op2
        else:
            registers[31]+=3

    # JLER
    elif cmd == 28:
        #print ("JLER:",cmd,op1,op2,"\n")
        if cc != 1:
            registers[31] = memory[registers[progCtr+2]]
        else:
            registers[31]+=3

    # JGE
    elif cmd == 29:
        #print ("JGE:",cmd,op1,op2,"\n")
        if cc != -1:
            registers[31] = op2
        else:
            registers[31]+=3

    # JGER
    elif cmd == 30:
        #print ("JGER:",cmd,op1,op2,"\n")
        if cc != -1:
            registers[31] = memory[registers[progCtr+2]]
        else:
            registers[31]+=3

    # JSUB
    elif cmd == 31:
        #print ("JSUB:",cmd,op1,op2,"\n")
        registers[memory[progCtr+1]] = registers[31]
        registers[31] = op2

    # JSUBR
    elif cmd == 32:
        #print ("JSUBR:",cmd,op1,op2,"\n")
        registers[memory[progCtr+1]] = registers[31]
        registers[31] = op2

    # HALT
    elif cmd == 33:
        #print ("HALT:",cmd,op1,op2,"\n")
        if go1 == True:
            go1 = False
            temp = copy.copy(registers)
            registers = copy.copy(waiting)
            waiting = copy.copy(temp)
        else:
            go2 = False

    # PREGS
    elif cmd == 34:
        #print("PREGS:",cmd,op1,op2,"\nPrinting registers starting at register",op2)
        x = op1
        y = 0
        while x <= op2:
            print (registers[x],end=" ")
            if y%8 == 0 and y!=0:
                print()
            x += 1
            y += 1
        print()
        registers[31]+=3

    # PINT
    elif cmd == 35:
        #print("PINT:",cmd,op1,op2,"\nPrinting memory starting at location", op2)
        x = op2
        y = 0
        while x < op2 + op1:
            print (memory[x],end=" ")
            if y%8 == 0 and y!=0:
                print()
            x += 1
            y += 1
        print()
        registers[31]+=3

    # multiprogramming switch
    if op == 2 and go1 == True:
        #print ("switch to other program\nsave current registers into temp")
        temp = copy.copy(registers)
        #print (registers,"\nload waiting into registers")
        registers = copy.copy(waiting)
        #print (registers,"load temp into waiting")
        waiting = copy.copy(temp)
        #print (waiting)
        op = 1
    elif op == 1 and go1 == True:
        op+=1


