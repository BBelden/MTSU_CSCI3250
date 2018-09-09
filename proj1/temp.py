#!/usr/bin/env python3.4

import sys

f = open(sys.argv[1])

for line in f:
    i = line.find("#")
    if i >= 0:
        line = line[:i]
    line = line.rstrip()
    if len(line) <= 0:
        continue
    sline = line.split()
    # print(sline)
    if not line[0].isspace():   # isalpha()
        label = sline[0]
        sline = sline[1:]   # sline is opcode and opt operands
    else:
        label = ""
    print(label,"    ",sline)
