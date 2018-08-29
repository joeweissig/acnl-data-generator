#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import sys
import os
from jinja2 import Environment, FileSystemLoader

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
    def uniquemonths(self):
        unique = []
        uniquenum = []
        for m in self.months:
            if m.number not in uniquenum:
                uniquenum.append(m.number)
                unique.append(m)
        return unique

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
    def name(self):
        if self.number == 13:
            return "island"
        else:
            return "month" + str(self.number)

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
            return self.ampm() + ": " + str(self.rarity)
    def ampm(self):
        if (self.allday):
            return "All Day"
        else:
            returnstr = ""
            if self.starthour == 0:
                returnstr += "Midnight - "
            elif self.starthour < 12:
                returnstr += str(self.starthour)
                returnstr += "am - "
            elif self.starthour == 12:
                returnstr += "Noon - "
            else:
                returnstr += str(self.starthour - 12)
                returnstr += "pm - "
            if self.endhour == 0:
                returnstr += "Midnight"
            elif self.endhour < 12:
                returnstr += str(self.endhour)
                returnstr += "am"
            elif self.endhour == 12:
                returnstr += "Noon"
            else:
                returnstr += str(self.endhour - 12)
                returnstr += "pm"
            return returnstr
    def classnames(self):
        if not self.allday:
            returnstr = ""
            if self.starthour < self.endhour:
                for h in range(self.starthour, self.endhour):
                    returnstr += "time" + str(h) + " "
            elif self.starthour > self.endhour:
                for h in range(self.starthour, self.endhour + 24):
                    returnstr += "time" + str(h % 24) + " "
            return returnstr

def makeBug(item):
    name_en = item['name']['en']
    name_jp = item['name']['jp']
    price = item['price']
    months = []
    if 'months' in item:
        for m in item['months']:
            spawn = m['spawn']
            for s in spawn:
                if m['month'] == 8 or m['month'] == 9:
                    if 'start' in m:
                        if m['start'] == 1:
                            if 'all_day' in s:
                                months.append(Month(m['month'], Time(True, 0, 0, s['rarity'])))
                            else:
                                months.append(Month(m['month'], Time(False, s['start'], s['end'], s['rarity'])))
                        elif m['start'] == 16:
                            if 'all_day' in s:
                                months.append(Month(m['month'] + 0.5, Time(True, 0, 0, s['rarity'])))
                            else:
                                months.append(Month(m['month'] + 0.5, Time(False, s['start'], s['end'], s['rarity'])))
                    else:
                        if 'all_day' in s:
                            months.append(Month(m['month'], Time(True, 0, 0, s['rarity'])))
                            months.append(Month(m['month'] + 0.5, Time(True, 0, 0, s['rarity'])))
                        else:
                            months.append(Month(m['month'], Time(False, s['start'], s['end'], s['rarity'])))
                            months.append(Month(m['month'] + 0.5, Time(False, s['start'], s['end'], s['rarity'])))
                else:
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

loader = FileSystemLoader('templates')
env = Environment(loader=loader)
template = env.get_template('template.html')

with open(str(sys.argv[1])[0:4] + ".html", "a") as myfile:
    for item in data:
        newbug = makeBug(item)
        myfile.write(template.render(Data=newbug, Type=str(sys.argv[1])[0:4]))
