#!/usr/bin/python
from random import randint
import sys

count = {}
description = {}
target = {}
lines = []
choices = [[]]
file = 'choice.test'
if sys.argv[1]:
    file = sys.argv[1]

def incfile(file):
#    print("file: " + file)
    fd = open(file)
    for line in fd.readlines():
        line = line.rstrip('\n')
        include = line.split()
        if include[0] == '#include':
            incfile(include[1])
        else:
            lines.append(line)
    fd.close()

def choose(item):
    section = len(choices) - 1
    if count.get(item, 0) == 0:
        print("item:", item, "is undefined")
        return
    pick = randint(0, count[item] - 1)
    choice = description[item][pick]
    nexts = target[item][pick]
#    print(item + " :" + choice)
    if choice.strip() == 'NONE':
        pass
    elif choice.strip()[0:8] == '--------':
        if len(choices[section]) > 0:
            choices.append([])
            section = len(choices)
    else:
        choices[section].append(item + " :" + choice)
    for nextchoice in nexts:
        choose(nextchoice.strip())
    return

def printChoices():
    for section in range(len(choices)):
        print(section)
        for row in range(len(choices[section])):
            print choices[section][row]

def testit():
    for key in target.keys():
        prev = ''
        for i in range(len(target[key])):
            nexts = target[key][i]
            for nextchoice in nexts:
                if prev != nextchoice:
                    if not nextchoice.strip() in target:
                        print("next:", nextchoice, "not found for", key)
                prev = nextchoice

incfile(file)
first = lines.pop(0).strip()
for line in lines:
#    print line
    nexts = line.split(',')
    item = nexts.pop(0)
    item = item.strip()
    odds = int(nexts.pop(0))
    desc = nexts.pop(0)
#    print("item:", item, "odds:", odds, "desc:", desc, "nexts:",nexts)
    for i in range(odds):
        count[item] = count.get(item, 0)
#        print("cnt[", item, "] =", count[item])
        description.setdefault(item,[]).append(desc)
        target.setdefault(item,[]).append(nexts)
        count[item] = count.get(item, 0) + 1
#print "=========================================="
#print description
#print count
#print "=========================================="
#for key in target.keys():
#    print("key:", key, "desc:", description[key])
#    print target[key]
testit()
choose(first)
printChoices()
exit
