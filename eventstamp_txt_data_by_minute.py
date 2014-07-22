'''
eventstamp_txt_data_by_minute.py

Sage Berg
Created May 2014
'''

from datetime             import *
from eventstamp_class     import *
from eventstamp_variables import *
from eventstamp_parser    import *

try:
    from personal_people_list import people
except:
    print('failed to import personal_people_list')

class Data_By_Minute(object):
    
    def __init__(self):
        self.eventstamp_list = make_eventstamp_list()

    def make_happiness_by_minute_file(self): 
        print('writing happiness_by_minute.txt')
        happiness_by_minute = open('data/happiness_by_minute.txt', 'w')
        happiness_by_minute_dict = dict()
        shortened_eventstamp_list = list() 
        #does not include stamps from today
        for i in range(len(self.eventstamp_list)):
            if self.eventstamp_list[i].date != \
               (date.today().year-2000, date.today().month, date.today().day):
                shortened_eventstamp_list.append(self.eventstamp_list[i])
        for minute in range(1,1441):
            happiness_by_minute_dict[minute] = list() 
            #holds a happiness value for each day for minute
        for i in range(1,len(shortened_eventstamp_list)): 
            #am I ignoring the last stamp?
            prev_stamp = \
            shortened_eventstamp_list[i-1].minute + \
            60*shortened_eventstamp_list[i-1].hour 
            curr_stamp = \
            shortened_eventstamp_list[i].minute   + \
            60*shortened_eventstamp_list[i].hour
            if shortened_eventstamp_list[i].what != 'Sleep': 
                if prev_stamp > curr_stamp:
                    prev_stamp -= 1440 #for crossing midnight
                for j in range(prev_stamp+1, curr_stamp+1):
                    happiness_by_minute_dict[j].append\
                    (shortened_eventstamp_list[i].happiness)
        for i in range(1,len(happiness_by_minute_dict)+1):
            sum_of_happiness_by_minute = 0
            divisor = 0 
            #equals days where there was a happiness score for this minute
            for j in range(1,len(happiness_by_minute_dict[i])):
                sum_of_happiness_by_minute += \
                int(happiness_by_minute_dict[i][j])
                divisor += 1
            if divisor == 0:
                divisor += 1 #hacky
            happiness_by_minute_dict[i] = \
            round(sum_of_happiness_by_minute/divisor,2)
            happiness_by_minute.write(str(i) + ', ' + \
            str(happiness_by_minute_dict[i]) + '\n')
        happiness_by_minute.close()              

    def make_by_minute_text_file(self): 
        '''reads eventstamp_data.txt
           writes time_use_by_minute.txt 
        '''
        print('writing time_use_by_minute.txt')
        raw_by_minute_file   = open('data/time_use_by_minute.txt',   'w')
        activity_minute_list = list() #holds data until it is written to file
        column_names = ''
        for h in range(len(event_list)): 
            #iterates list of tuples to collect column titles
            #and add 1440 item minute lists to activity_minute_list 
            activity_minute_list.append([0 for i in range(1440)])
            column_names += event_map[h] + ', '
        raw_by_minute_file.write(column_names[:-2] + '\n')        
        for i in range(1,len(self.eventstamp_list)): #i is the eventstamp index
            end_minute   = self.eventstamp_list[i].hour*60   + \
                           self.eventstamp_list[i].minute 
            begin_minute = self.eventstamp_list[i-1].hour*60 + \
                           self.eventstamp_list[i-1].minute
            if end_minute < begin_minute:
                begin_minute -= 1440 #deals with midnight
            for j in range(begin_minute, end_minute): #j is the minute index 
                activity_minute_list[inverted_event_map\
                [self.eventstamp_list[i].what.strip().lower()]][j] += 1
        for k in range(1440):
            number_string = ''
            for m in range(len(event_list)): 
                number_string += str(activity_minute_list[m][k]) + ',' 
                #index by activity m, then by minute k
            raw_by_minute_file.write(number_string[:-1] + '\n')
        raw_by_minute_file.close()

def main():
    x = Data_By_Minute()
    x.make_happiness_by_minute_file()
    x.make_by_minute_text_file()
