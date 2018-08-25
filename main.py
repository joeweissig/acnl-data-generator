#!/usr/bin/python3

# coding = UTF8

import json
import sys
import os
# from enum import Enum

class Bug:
    def __init__(self, name_en, name_jp, price, months):
        self.name_en = name_en
        self.name_jp = name_jp
        self.price = price
        self.months = months
    def __repr__(self):
        bugstr = ""
        bugstr += self.name_en + " ("
        bugstr += self.name_jp + "): "
        # bugstr += self.name_en + ": "
        bugstr += str(self.price) + " Bells.\n"
        for m in self.months:
            bugstr += str(m) + "\n"
        return bugstr
    def toHTML(self):
        html = ""

class Month:
    # month number 13 will stand for the island
    def __init__(self, number, *times):
        self.number = number
        self.times = times
    def __repr__(self):
        for t in self.times:
            if self.number == 13:
                return "Island: " + str(t)
            else:
                return str(self.number) + ": " + str(t)

# class Rarity(Enum):
#     VERY_COMMON = 1
#     COMMON = 2
#     RARE = 3
#     VERY_RARE = 4

class Time:
    def __init__(self, allday, starthour, endhour, rarity):
        self.allday = allday
        self.starthour = starthour
        self.endhour = endhour
        self.rarity = rarity
    def __repr__(self):
        if self.allday:
            return "All day: " + str(self.rarity)
        else:
            return str(self.starthour) + "00 - " + str(self.endhour) + "00: " + str(self.rarity)

def makeBug(item):
    name_en = item['name']['en']
    name_jp = item['name']['jp']
    price = item['price']
    months = []
    print(name_en)
    if 'months' in item:
        for m in item['months']:
            spawn = m['spawn']
            for s in spawn:
                if 'all_day' in s:
                    months.append(Month(m['month'], Time(True, 0, 0, s['rarity'])))
                else:
                    months.append(Month(m['month'], Time(False, s['start'], s['end'], s['rarity'])))
    if 'island' in item:
        island = item['island']
        for i in island:
            if 'all_day' in i:
                months.append(Month(13, Time(True, 0, 0, i['rarity'])))
            else:
                months.append(Month(13, Time(False, i['start'], i['end'], i['rarity'])))
    return Bug(name_en, name_jp, price, months)

    



if len(sys.argv) > 1:
    with open(sys.argv[1], encoding='utf-8') as f:
        data = json.load(f)
elif len(sys.argv) == 1:
    print("Pass the requested JSON file path as a command line argument")
    exit()

buglist = []

for item in data:
    buglist.append(makeBug(item))

for bug in buglist:
    print(bug)

