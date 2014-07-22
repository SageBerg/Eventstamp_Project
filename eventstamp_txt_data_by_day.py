'''
eventstamp_txt_data_by_day.py

Sage Berg
Created March 2014
'''

from datetime             import *
from eventstamp_class     import *
from eventstamp_variables import *
from eventstamp_parser    import *

try:
    from personal_people_list import people
except:
    print('failed to import personal_people_list.py')

class Data_By_Day(object):

    def __init__(self):
        self.eventstamp_list = make_eventstamp_list()
        self.date_dict       = make_date_dict()

    def make_date_string(self, index):
        date_string = str(self.date_dict[index][1]) + '/'   + \
                      str(self.date_dict[index][2]) + '/20' + \
                      str(self.date_dict[index][0])
        return date_string
    
    def make_time_use_by_day_file(self): 
        time_use_by_day = open('data/time_use_by_day.txt', 'w') 
        time_use_by_day.write('DATE, ') 
        for activity in event_list:
            time_use_by_day.write(activity[0] + ',') 
            #write column names to text file
        time_use_by_day.write('\n')

        for i in range(len(self.date_dict)): 
            date_string = self.make_date_string(i)
            time_use_by_day.write(date_string + ',')
            time_use_dict = {activity[0].title():0 for activity in event_list}
            for j in range(len(self.eventstamp_list)): #stupid loop, fix
                if j == 0 and self.date_dict[i] == self.eventstamp_list[j].date:
                    duration = self.eventstamp_list[j].minute + \
                               self.eventstamp_list[j].hour*60
                    time_use_dict[self.eventstamp_list[j].what.strip()] += duration
                elif self.date_dict[i] == self.eventstamp_list[j].date:
                    duration = get_eventstamp_duration(j, self.eventstamp_list)
                    time_use_dict[self.eventstamp_list[j].what.strip()] += duration
            daily_activity_list = [ (activity[0].title(), time_use_dict[activity[0].title() ]) \
                                    for activity in event_list]
            for tup in daily_activity_list: 
                time_use_by_day.write(str(tup[1]) + ',')
            time_use_by_day.write('\n')

        time_use_by_day.close()

    def make_happiness_by_day_file(self):
        average_happiness_by_day = open('data/happiness_by_day.txt', 'w')
        for i in range(len(self.date_dict)): 
            date_string = self.make_date_string(i)
            average_happiness_by_day.write(date_string + ',')
            day_happiness_sum = 0
            divisor = 0
            for j in range(1, len(self.eventstamp_list)):
                if self.date_dict[i] == self.eventstamp_list[j].date and \
                   self.eventstamp_list[j].what != 'Sleep':
                    duration = get_eventstamp_duration(j, self.eventstamp_list)
                    day_happiness_sum += \
                    int(self.eventstamp_list[j].happiness.strip())*duration
                    divisor += duration
            try:
                average = day_happiness_sum/divisor
            except:
                print('average happiness = day_hapiness_sum/zero')
            average = round(average,3)
            average_happiness_by_day.write(str(average) + '\n')
        average_happiness_by_day.close()

    def make_people_time_dict(self, people_list): 
        '''called by make_people_by_day_file'''

        return {person : 0 for person in people_list}

    def make_people_by_day_file(self): 
        people_by_day = open('data/people_by_day.txt', 'w')
        days_dict = dict()
        for i in range(len(self.eventstamp_list)):
            if self.eventstamp_list[i].date not in days_dict:
                days_dict[self.eventstamp_list[i].date] = \
                self.make_people_time_dict(people)
            for person in self.eventstamp_list[i].who.split():
                if person in self.make_people_time_dict(people):
                    duration = get_eventstamp_duration(i, self.eventstamp_list)
                    days_dict[self.eventstamp_list[i].date][person] += duration 
        people_columns_string = 'DATE, ' 
        for person in people:
            people_columns_string += person + ', '
        people_by_day.write(people_columns_string[:-2] + '\n')
        for i in range(len(self.date_dict)):
            date_string = str(self.date_dict[i]) + ', '
            for person in people:
                date_string += str(days_dict[self.date_dict[i]][person]) + ', '
            people_by_day.write(date_string[:-2] + '\n')
        people_by_day.close()

    def make_stress_by_day_file(self): 
        stress_by_day = open('data/stress_by_day.txt', 'w') 
        for i in range(len(self.date_dict)): 
            date_string = self.make_date_string(i)
            stress_by_day.write(date_string + ', ')
            stress_minute_sum = 0
            for j in range(1, len(self.eventstamp_list)): 
                if self.date_dict[i] == self.eventstamp_list[j].date and \
                   self.eventstamp_list[j].stress == 1:
                    duration = get_eventstamp_duration(i, self.eventstamp_list)
                    stress_minute_sum += duration
            stress_by_day.write(str(stress_minute_sum) + '\n')
        stress_by_day.close()

    def make_stamps_by_day_file(self):
        f = open('data/stamps_by_day.txt', 'w')
        fragment_dict = dict()
        for eventstamp in self.eventstamp_list:
            if eventstamp.date not in fragment_dict:
                fragment_dict[eventstamp.date] = 1
            else:
                fragment_dict[eventstamp.date] += 1
        date_list = list()
        for key in fragment_dict:
            date_list.append([key, fragment_dict[key]])
        date_list.sort()
        for date in date_list:
            f.write(str(date[0][2]) + "-" + str(month_dict[date[0][1]]) + \
            "-20" + str(date[0][0]) + ", " + str(date[1]) + "\n") 
        f.close()

def main():
    x = Data_By_Day()
    x.make_happiness_by_day_file()
    x.make_stress_by_day_file()
    x.make_time_use_by_day_file()
    x.make_stamps_by_day_file()
    x.make_people_by_day_file()
