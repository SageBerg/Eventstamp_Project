'''
eventstamp_txt_data_by_day.py

Sage Berg
Created ?? March 2014
'''

import eventstamp_parser
import eventstamp_variables
from datetime             import *
from eventstamp_class     import *
from eventstamp_variables import *

try:
    from personal_people_list import people
except:
    print('failed to import personal_people_list')

eventstamp_list = eventstamp_parser.make_eventstamp_list()
date_dict = eventstamp_parser.make_date_dict()
    
def make_time_use_by_day_file():
    time_use_by_day = open('data/time_use_by_day.txt', 'w') 
    for activity in eventstamp_variables.event_list:
        time_use_by_day.write(activity[0] + ',') #write column names to text file
    time_use_by_day.write('\n')

    for i in range(len(date_dict)): 
        daily_time_use_dict = {activity[0].title():0 for activity in eventstamp_variables.event_list}
        for j in range(1, len(eventstamp_list)): #stupid loop, fix
            if date_dict[i] == eventstamp_list[j].date:
                curr_time = 60*eventstamp_list[j].hour + eventstamp_list[j].minute 
                prev_time = 60*eventstamp_list[j-1].hour + eventstamp_list[j-1].minute
                duration = curr_time - prev_time
                if duration < 0:
                    duration += 1440 
                daily_time_use_dict[eventstamp_list[j].what.strip()] += duration
        daily_activity_list = [(activity[0].title(), \
        daily_time_use_dict[activity[0].title()]) for activity in eventstamp_variables.event_list]
        for tup in daily_activity_list: 
            time_use_by_day.write(str(tup[1]) + ',')
        time_use_by_day.write('\n')
    time_use_by_day.close()

def make_average_happiness_by_day_file():
    average_happiness_by_day = open('data/happiness_by_day.txt', 'w')
    for i in range(len(date_dict) -1): #don't indluce current date, since the happiness total is not yet known
        date_string = str(date_dict[i][1]) + '/' + str(date_dict[i][2]) + '/20' + str(date_dict[i][0])
        average_happiness_by_day.write(date_string + ',')
        day_happiness_sum = 0
        divisor = 0
        for j in range(1, len(eventstamp_list)):
            if date_dict[i] == eventstamp_list[j].date and eventstamp_list[j].what != 'Sleep':
                curr_time = 60*eventstamp_list[j].hour + eventstamp_list[j].minute 
                prev_time = 60*eventstamp_list[j-1].hour + eventstamp_list[j-1].minute
                duration = curr_time - prev_time
                if duration < 0:
                    duration += 1440 
                day_happiness_sum += int(eventstamp_list[j].happiness.strip())*duration
                divisor += duration
        average = day_happiness_sum/divisor
        average = round(average,3)
        average_happiness_by_day.write(str(average) + '\n')
    average_happiness_by_day.close()

def make_people_time_dict(people_list): #called by make_people_by_day_file
    return {person : 0 for person in people_list}

def make_people_by_day_file(): 
    people_by_day = open('data/people_by_day.txt', 'w')
    days_dict = dict()
    for i in range(len(eventstamp_list)):
        if eventstamp_list[i].date not in days_dict:
            days_dict[eventstamp_list[i].date] = make_people_time_dict(people)
        for person in eventstamp_list[i].who.split():
            if person in make_people_time_dict(people):
                duration = eventstamp_parser.get_eventstamp_duration(i, eventstamp_list)
                days_dict[eventstamp_list[i].date][person] += duration 
    people_columns_string = "DATE, "
    for person in people:
        people_columns_string += person + ', '
    people_by_day.write(people_columns_string[:-2] + '\n')
    for i in range(len(date_dict)):
        date_string = str(date_dict[i]) + ', '
        for person in people:
            date_string += str(days_dict[date_dict[i]][person]) + ', '
        people_by_day.write(date_string[:-2] + '\n')
    people_by_day.close()

def make_stress_percent_by_day_file(): #change to raw minutes
    stress_percent_by_day = open('data/stress_percent_by_day.txt', 'w') 
    for i in range(len(date_dict)): 
        date_string = str(date_dict[i][1]) + '/' + str(date_dict[i][2]) + '/20' + str(date_dict[i][0])
        stress_percent_by_day.write(date_string + ',')
        stress_minute_sum = 0
        for j in range(1, len(eventstamp_list)): 
            if date_dict[i] == eventstamp_list[j].date and eventstamp_list[j].stress == 1:
                curr_time = 60*eventstamp_list[j].hour + eventstamp_list[j].minute 
                prev_time = 60*eventstamp_list[j-1].hour + eventstamp_list[j-1].minute
                duration = curr_time - prev_time
                if duration < 0:
                    duration += 1440 
                stress_minute_sum += duration
        percent = 100*(stress_minute_sum/1440)
        average = round(percent,0)
        stress_percent_by_day.write(str(average) + '%\n')
    stress_percent_by_day.close()

def make_stamps_by_day_file():
    f = open('data/stamps_by_day.txt', 'w')
    fragment_dict = dict()
    for eventstamp in eventstamp_list:
        if eventstamp.date not in fragment_dict:
            fragment_dict[eventstamp.date] = 1
        else:
            fragment_dict[eventstamp.date] += 1
    date_list = list()
    for key in fragment_dict:
        date_list.append([key, fragment_dict[key]])
    date_list.sort()
    for date in date_list:
        f.write(str(date[0][2]) + "-" + str(eventstamp_variables.month_dict[date[0][1]]) + \
        "-20" + str(date[0][0]) + ", " + str(date[1]) + "\n") 
    f.close()

def main():
    make_average_happiness_by_day_file()
    make_stress_percent_by_day_file()
    make_time_use_by_day_file()
    make_stamps_by_day_file()
    make_people_by_day_file()
