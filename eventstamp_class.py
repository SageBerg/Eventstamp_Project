class Eventstamp(object):

    def __init__(self, year, month, day, hour, minute, what, who, happiness, note, where, stress):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.date = (year, month, day) #used in eventstamp_averages.py
        
        self.who = who

        self.what = what
        self.note = note

        self.where = where

        self.happiness = happiness
        if stress.strip() == 'stress':
            self.stress = 1
        else:
            self.stress = 0

    def __str__(self):
        return str(self.year) + ', ' + \
               str(self.month) + ', ' + \
               str(self.day) + ', ' + \
               str(self.hour) + ', ' + \
               str(self.minute) + ', ' + \
               self.what + ', ' + \
               self.who + ', ' + \
               str(self.happiness) + ', ' + \
               str(self.where) + ', ' + \
               str(self.stress)
