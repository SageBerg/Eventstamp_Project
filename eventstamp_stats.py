'''
eventstamp_stats.py

Design Goal:

update_by_minute_table    updates by_minute table in eventstamp.db
                          updates by_minute.txt 
make_by_hour_table
make_by_day_table
make_by_week_table
make_by_month_table
make_by_quarter_table
main                    calls all other functions in program

idea:   have eventstamp.py run eventstamp_stats on launch

Sage Berg
Created ?? March 2014
Edited  11 June  2014
'''

import eventstamp_parser
import eventstamp_variables
import sqlite3
from datetime             import *
from eventstamp_class     import *
from eventstamp_variables import *

eventstamp_list = eventstamp_parser.make_eventstamp_list()
eventstamp_list.insert(0,Eventstamp(14,3,5,0,0,'Other', '', 3, '', '', 'no stress'))
date_dict = eventstamp_parser.make_date_dict()

try:
    con = sqlite3.connect('stats.db')
    cur = con.cursor()
except sqlite3.Error:
    sys.exit(1)

def make_happiness_by_minute_file(): #lots of off-by-one screw ups, but it probably provides the right output
    print('writing happiness_by_minute.txt')
    happiness_by_minute = open('Eventstamp_Stats/happiness_by_minute.txt', 'w')
    happiness_by_minute_dict = dict()
    shortened_eventstamp_list = list() #does not include stamps from today
    for i in range(len(eventstamp_list)):
        if eventstamp_list[i].date != (date.today().year-2000, date.today().month, date.today().day):
            shortened_eventstamp_list.append(eventstamp_list[i])
    for minute in range(1,1441):
        happiness_by_minute_dict[minute] = list() #holds a happiness value for each day for minute
    for i in range(1,len(shortened_eventstamp_list)): #am I ignoring the last stamp?
        prev_stamp = shortened_eventstamp_list[i-1].minute + 60*shortened_eventstamp_list[i-1].hour 
        curr_stamp = shortened_eventstamp_list[i].minute   + 60*shortened_eventstamp_list[i].hour
        if shortened_eventstamp_list[i].what != 'Sleep': 
            if prev_stamp > curr_stamp:
                prev_stamp -= 1440 #for crossing midnight
            for j in range(prev_stamp+1, curr_stamp+1):
                happiness_by_minute_dict[j].append(shortened_eventstamp_list[i].happiness)
    for i in range(1,len(happiness_by_minute_dict)+1):
        sum_of_happiness_by_minute = 0
        divisor = 0 #will equal total days for which there was a happiness score for this minute
        for j in range(1,len(happiness_by_minute_dict[i])):
            sum_of_happiness_by_minute += int(happiness_by_minute_dict[i][j])
            divisor += 1
        if divisor == 0:
            divisor += 1 #hacky
        happiness_by_minute_dict[i] = round(sum_of_happiness_by_minute/divisor,2)
        happiness_by_minute.write(str(i) + ', ' + str(happiness_by_minute_dict[i]) + '\n')
    happiness_by_minute.close()              

def update_by_minute_text_file(): 
    '''reads eventstamp_data.txt
       writes by_minute text files
    '''
    print('writing by_minute.txt files')
    raw_by_minute_file   = open('Eventstamp_Stats/raw_by_minute.txt',   'w')
    ratio_by_minute_file = open('Eventstamp_Stats/ratio_by_minute.txt', 'w')
    activity_minute_list = list() #holds data until it is writen to file
    column_names = ''
    for h in range(len(eventstamp_variables.event_list)): 
        #iterates list of tuples to collect column titles
        #and add 1440 item minute lists to activity_minute_list 
        activity_minute_list.append([0 for i in range(1440)])
        column_names += eventstamp_variables.event_map[h] + ', '
    raw_by_minute_file.write(column_names[:-2] + '\n')        
    ratio_by_minute_file.write(column_names[:-2] + '\n')        
    for i in range(1,len(eventstamp_list)): #i is the eventstamp index
        end_minute   = eventstamp_list[i].hour*60   + eventstamp_list[i].minute 
        begin_minute = eventstamp_list[i-1].hour*60 + eventstamp_list[i-1].minute
        if end_minute < begin_minute:
            begin_minute -= 1440 #deals with midnight
        for j in range(begin_minute, end_minute): #j is the minute index 
            activity_minute_list[eventstamp_variables.inverted_event_map[eventstamp_list[i].what.strip().lower()]][j] += 1
    ratio_activity_minute_list = list()
    for item in activity_minute_list:
        ratio_activity_minute_list.append(item[:]) #make deep copies
    divisor = len(date_dict)
    for a in range(len(eventstamp_variables.event_list)):
        for b in range(1440):
            ratio_activity_minute_list[a][b] /= divisor
    for k in range(1440):
        number_string = ''
        for m in range(len(eventstamp_variables.event_list)): 
            number_string += str(activity_minute_list[m][k]) + ',' #index by activity m, then by minute k
        raw_by_minute_file.write(number_string[:-1] + '\n')
    for p in range(1440):
        number_string = ''
        for q in range(len(eventstamp_variables.event_list)):
            number_string += str(ratio_activity_minute_list[q][p]) + ','
        ratio_by_minute_file.write(number_string[:-1] + '\n')
    raw_by_minute_file.close()
    ratio_by_minute_file.close()

def make_day_table():
    sql_string = 'CREATE TABLE day(id INT, date TEXT, '
    for i in range(len(eventstamp_variables.event_list)):
        activity = eventstamp_variables.event_list[i][0]
        activity = activity.replace(' ', '_').replace('&','').replace('-','_').title() 
        sql_string += activity + ' TEXT, '
    sql_string += 'stamps INT, '
    sql_string += 'happiness FLOAT, '
    sql_string = sql_string[:len(sql_string) -2] + ');'
    print(sql_string)
    cur.executescript('DROP TABLE IF EXISTS day;' + sql_string)

    date_list = list()
    for i in range(len(date_dict)):
        date_list.append(date_dict[i])
    date_list.sort()

    for i in range(len(date_list)):
        cur.execute('INSERT INTO day (id, date) VALUES (\'' + str(i) + '\', \'' + str(date_list[i]) + '\');')
    con.commit()

def make_empty_time_use_by_day_dict():
    return {activity[0].title(): 0 for activity in eventstamp_variables.event_list}

def update_time_use_by_day_columns():
    time_use_for_all_days_dict = dict() #dict maps dates to dicts that map activities to time totals
    for i in range(len(eventstamp_list)):
        if eventstamp_list[i].date not in time_use_for_all_days_dict:
            time_use_for_all_days_dict[eventstamp_list[i].date] = make_empty_time_use_by_day_dict()
        else:
            last_time = eventstamp_list[i-1].hour*60 + eventstamp_list[i-1].minute
            curr_time = eventstamp_list[i].hour*60   + eventstamp_list[i].minute 
            duration  = curr_time - last_time
            if duration < 0:
                duration += 1440
            time_use_for_all_days_dict[eventstamp_list[i].date][eventstamp_list[i].what] += duration

    for date in date_dict.values(): 
        for activity in time_use_for_all_days_dict[date]:
            q = 'UPDATE day SET ' + \
            activity .replace(' ', '_').replace('&','').replace('-','_').title() + \
            ' = \'' + str(time_use_for_all_days_dict[date][activity]) + \
            '\' WHERE date = \'' + str(date) + '\';'
            cur.execute(q)
    con.commit()

def update_stamps_by_day_column():
    stamps_by_day_dict = dict()
    for i in range(len(eventstamp_list)):
        if eventstamp_list[i].date not in stamps_by_day_dict:
            stamps_by_day_dict[eventstamp_list[i].date] = 1
        else:
            stamps_by_day_dict[eventstamp_list[i].date] += 1
    for date in stamps_by_day_dict:
        q = 'UPDATE day SET ' + \
        'stamps = \'' + str(stamps_by_day_dict[date]) +\
        '\' WHERE date = \'' + str(date) + '\';'
        cur.execute(q)
    con.commit()

def update_average_happiness_by_day_column():
    hap_by_day_dict = dict()
    for date in date_dict.values():
        if date not in hap_by_day_dict:
            hap_by_day_dict[date] = 0 
    for i in range(len(date_dict)): 
        day_happiness_sum = 0
        divisor = 0
        for j in range(1, len(eventstamp_list)): #bad loop
            if date_dict[i] == eventstamp_list[j].date and eventstamp_list[j].what != 'Sleep':
                curr_time = 60*eventstamp_list[j].hour + eventstamp_list[j].minute 
                prev_time = 60*eventstamp_list[j-1].hour + eventstamp_list[j-1].minute
                duration = curr_time - prev_time
                if duration < 0:
                    duration += 1440 
                day_happiness_sum += int(eventstamp_list[j].happiness.strip())*duration
                divisor += duration
        if divisor == 0: #tacky
            divisor += 1
        average = day_happiness_sum/divisor
        average = round(average,3)
        hap_by_day_dict[date_dict[i]] = average
    for date in hap_by_day_dict:
        q = 'UPDATE day SET ' + \
        'happiness = \'' + str(hap_by_day_dict[date]) +\
        '\' WHERE date = \'' + str(date) + '\';'
        cur.execute(q)
    con.commit()
    
def make_time_use_by_day_file():
    time_use_by_day = open('Eventstamp_Stats/time_use_by_day.txt', 'w') 
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
    average_happiness_by_day = open('Eventstamp_Stats/average_happiness_by_day.txt', 'w')
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

def make_stress_percent_by_day_file():
    stress_percent_by_day = open('Eventstamp_Stats/stress_percent_by_day.txt', 'w') 
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

def make_fragmentation_by_day_file():
    f = open('Eventstamp_Stats/fragmentation_by_day.txt', 'w')
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

def following():
    print('writing following.txt')

    activity_dict = dict()
    
    for i in range(len(event_list)):
        activity_dict[event_list[i][0].title()] = dict()
        for j in range(len(event_list)):
            activity_dict[event_list[i][0].title()][event_list[j][0].title()] = 0

    for k in range(len(eventstamp_list) -1):
        cur = eventstamp_list[k].what
        nex = eventstamp_list[k+1].what
        activity_dict[cur][nex] += 1

    outfile = open('Eventstamp_Stats/following.txt', 'w')

    column_titles_string = ', '
    for l in range(len(event_list)):
        column_titles_string += event_list[l][0].title() + ', '
    outfile.write(column_titles_string + '\n')

    for m in range(len(event_list)):
        outfile.write(event_list[m][0].title() + ', ')
        for n in range(len(event_list)):
            outfile.write(str(activity_dict[event_list[m][0].title()][event_list[n][0].title()]) + ', ')
        outfile.write('\n')
    outfile.close()

def main():
    make_day_table()
    make_happiness_by_minute_file()
    update_by_minute_text_file()
    make_average_happiness_by_day_file()
    make_stress_percent_by_day_file()
    make_time_use_by_day_file()
    make_fragmentation_by_day_file()
   #make_people_by_day_file()
    following()
    update_time_use_by_day_columns()    
    update_stamps_by_day_column()
    update_average_happiness_by_day_column()

main()

con.close()
