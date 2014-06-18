'''
eventstamp_sql_data_by_day.py

Sage Berg
Created 13 June 2014
'''

import sqlite3
from datetime             import *
from eventstamp_class     import *
from eventstamp_variables import *
from eventstamp_parser    import *

try:
    from personal_people_list import people
except:
    print('failed to import personal_people_list')

eventstamp_list = make_eventstamp_list()
date_dict       = make_date_dict()

try:
    con = sqlite3.connect('data/eventstamp_statistics.db')
    cur = con.cursor()
except sqlite3.Error:
    sys.exit(1)

def make_day_table():
    sql_string = 'CREATE TABLE day(id INT, date TEXT, '
    for i in range(len(event_list)):
        activity = event_list[i][0]
        activity = \
        activity.replace(' ', '_')  \
                .replace('&','And') \
                .replace('-','_')   \
                .title()  
        sql_string += activity + ' TEXT, '
    sql_string += 'stamps INT, '
    sql_string += 'happiness FLOAT, '
    sql_string = sql_string[:len(sql_string) -2] + ');'
    print('writing eventstamp_stats.db')
    cur.executescript('DROP TABLE IF EXISTS day;' + sql_string)

    date_list = list()
    for i in range(len(date_dict)):
        date_list.append(date_dict[i])
    date_list.sort()

    for i in range(len(date_list)):
        cur.execute('INSERT INTO day (id, date) VALUES (\'' + \
                    str(i) + '\', \'' + str(date_list[i]) + '\');')
    con.commit()

def make_empty_time_use_by_day_dict():
    return {activity[0].title(): 0 for activity in event_list}

def update_time_use_by_day_columns():
    time_use_for_all_days_dict = dict() 
    #dict maps dates to dicts that map activities to time totals
    for i in range(len(eventstamp_list)):
        if eventstamp_list[i].date not in time_use_for_all_days_dict:
            time_use_for_all_days_dict[eventstamp_list[i].date] = \
            make_empty_time_use_by_day_dict()
        else:
            duration = get_eventstamp_duration(i, eventstamp_list)
            time_use_for_all_days_dict[eventstamp_list[i].date]\
            [eventstamp_list[i].what] += duration

    for date in date_dict.values(): 
        for activity in time_use_for_all_days_dict[date]:
            q = 'UPDATE day SET ' +     \
            activity.replace(' ', '_')  \
                    .replace('&','And') \
                    .replace('-','_')   \
                    .title() + \
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
            if date_dict[i] == eventstamp_list[j].date and \
               eventstamp_list[j].what != 'Sleep':
                duration = get_eventstamp_duration(j, eventstamp_list)
                day_happiness_sum += \
                int(eventstamp_list[j].happiness.strip())*duration
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

def main():
    try:
        con = sqlite3.connect('data/eventstamp_statistics.db')
        cur = con.cursor()
    except sqlite3.Error:
        sys.exit(1)

    make_day_table()
    update_time_use_by_day_columns()    
    update_stamps_by_day_column()
    update_average_happiness_by_day_column()
    con.close()
