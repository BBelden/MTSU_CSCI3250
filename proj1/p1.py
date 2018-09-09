#!/usr/bin/env python3.4

import sys



f = open(sys.argv[1])
ttlSymbls = 0
locCtr = 0
tmpCtr = 0
lblType = "rel"
symbols = []


def addToTable(x,y,z):
    symbols.append([x,y,z])
    #print(x,y,z)

# function strOrInt
# takes in a string, returns a value to be added to location counter
def strOrInt(s):
    # if string is not an integer
    if not s.isdigit():
        # if string is an $, 0 value returned
        if s == "$":
            return locCtr
        # else get value from symbol table
        else:
            for row in symbols:
                if row[0] == s:
                    return row[1]       
    # if string is an integer
    if s.isdigit():
        return int(s)

# function arithmetic
# takes in a string, returns an integer value
def arithmetic(s):
    plus = s.find('+')
    minus = s.find('-')
    if plus >=0:
        lftOp = strOrInt(s[0:plus])
        rtOp = strOrInt(s[plus+1:len(s)])
        val = lftOp + rtOp
        return val
    if minus>=0:
        lftOp = strOrInt(s[0:minus])
        rtOp = strOrInt(s[minus+1:len(s)])
        val = lftOp - rtOp
        return val
    else:
        return strOrInt(s)
    
 
def relOrAbs(s):
    if s.isdigit():
        lbl = "abs"
    else:
        lbl = "rel"
    return lbl
#def isrelative(val):
#if val[0].isdigit():
#return false
#else:
#if value in table for that label == rel
#return true
#else:
#return false


for line in f:
    i = line.find("#")
    if i >= 0:
        line = line[:i]
    line = line.rstrip()
    if len(line) <= 0:
        continue
    sline = line.split()
    if not line[0].isspace():
        label = sline[0]
        sline = sline[1:]
    else:
        label = ""
    cmd = sline[0]
    sline = sline[1:]
    if len(sline) <= 0:
        args = ""
    else:
        args = sline[0]
    
    #org
    if cmd == "ORG":
        locCtr = arithmetic(args)
    
    #equ
    elif cmd == "EQU":
        lblType = relOrAbs(args)
        addToTable(label,arithmetic(args),lblType)
 
    #intu,intz
    elif cmd == "INTZ" or cmd == "INTU":
        lblType = "rel"
        addToTable(label,locCtr,lblType)
        locCtr += int(args) 
    
    # int
    elif cmd == "INT":
        lblType = "rel"
        addToTable(label,locCtr,lblType)
        locCtr += 1
    
    # all others    
    else:
        lblType = "rel"
        if label != "":
            addToTable(label,locCtr,lblType)
        locCtr += 3

for row in symbols:
    print("    {: <7}{: >4}{: >4}".format(*row))

# print sample output
print("\nSample output:")
myfile = open("p1a.txt")
for line in myfile:
    line = line.rstrip()
    print(line)

