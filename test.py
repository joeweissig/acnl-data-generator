# coding: iso-8859-15

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


# birdwingbutterfly = Bug("Birdwing Butterfly", "アレクサンドラアゲハ", 4000, [Month(6, [Time(False, 8, 16, Rarity.VERY_RARE)]), Month(7, [Time(False, 8, 16, Rarity.VERY_RARE)]), Month(8, [Time(False, 8, 16, Rarity.VERY_RARE)]), Month(9, [Time(False, 8, 16, Rarity.VERY_RARE)]), Month(13, [Time(False, 8, 16, Rarity.VERY_RARE)])])
birdwingbutterfly = Bug("Birdwing Butterfly", "アレクサンドラアゲハ", 4000, [Month(6, [Time(False, 8, 16, "very rare")]), Month(7, [Time(False, 8, 16, "very rare")]), Month(8, [Time(False, 8, 16, "very rare")]), Month(9, [Time(False, 8, 16, "very rare")]), Month(13, [Time(False, 8, 16, "very rare")])])
print(birdwingbutterfly)

