'''
eventstamp_functions.py
this file imported by eventstamp_gui.py
to map functions as callbacks for gui buttons

Sage Berg
Created 10 April 2014
'''

from multiprocessing import Process 
from datetime import *
from eventstamp_variables import *
import eventstamp_parser 

import eventstamp_txt_data_following 
import eventstamp_txt_data_by_minute
import eventstamp_txt_data_by_day
import eventstamp_sql_data_by_day

try:
    from personal_depricated_notes import depricated_notes
except:
    print("failed to import personal_depricated_notes")
    depricated_notes = list() #make a dummy list to avoid reference errors

try:
    from personal_people_list import people
except:
    print("failed to import personal_people_list")
    people = list() #make a dummy list to avoid reference errors

def make_people_string(people_list): #used by draw_activity buttons
    people_string = ''
    for person in people_list:
         if person[1].get():
            people_string += person[0] + ' '
    return people_string

def remove_last_stamp_from_display(display, display_list):
    display.delete(display_list[-1])

def add_to_realtime_eventstamp_display(display, display_list):
    eventstamp_list = eventstamp_parser.make_eventstamp_list()
    color = 'black'
    for event in event_list: #tacky code
        if eventstamp_list[-1].what.lower() == event[0]:
            color = event[1]
    start_x = eventstamp_list[-2].minute + eventstamp_list[-2].hour*60
    end_x   = eventstamp_list[-1].minute + eventstamp_list[-1].hour*60 
    display_list.append(display.create_rectangle(start_x, 0, end_x, 40, \
                        fill=color, width=0))

def write_eventstamp(activity_string, people_string, happiness, note, \
                     where, stress, scales, scales_list, display, \
                     display_list):
    outfile   = open('eventstamp_data.txt', 'a')
    if scales.get():
        minute = zero_padder(scales_list[0].get())
        hour   = zero_padder(scales_list[1].get())
        day    = zero_padder(scales_list[2].get())
        month  = zero_padder(scales_list[3].get())
        year   = str(scales_list[4].get())
        timestamp = year + '-' + month + '-' + day + ' ' + \
                    hour + ':' + minute + ':00.000000'
    else:
        timestamp = str(datetime.today())
    activity  = activity_string
    people    = people_string
    mood      = str(happiness.get())
    stress_string = stress
    if stress.get() == 1:
        stress_string = 'stress'
    else:
        stress_string = 'no stress'
    outfile.write(timestamp + ', ' + activity_string + ', ' \
                   + people_string + ', ' + mood + ', ' + note \
                    + ', ' + where + ', ' + stress_string + '\n')
    outfile.close() 
    
    add_to_realtime_eventstamp_display(display, display_list)

def zero_padder(n):
    '''takes int, returns string'''
    if n < 10:
        return '0' + str(n)
    return str(n)   

def undo(display, display_list): #callback for "delete last stamp" button
    lines  = open('eventstamp_data.txt', 'r').readlines()
    line_cnt = 0
    for line in lines:
        line_cnt += 1
    open('eventstamp_data.txt', 'w').writelines(lines[:line_cnt-1])

    remove_last_stamp_from_display(display, display_list)

def get_last_stamp():
    lines  = open('eventstamp_data.txt', 'r').readlines()
    return lines[-1][5:16] + lines[-1][26:-14] 
    #get the last line and don't include it's \n

def make_note_shortcut_list(eventstamp_list): 
    #function needs a clean up (bad name)
    #changes number of note buttons that appear when eventstamp.py is run
    number_of_note_shortcuts = 56 #most common non-depricated notes
    frequent_note_dict = dict()
    for eventstamp in eventstamp_list: 
        if eventstamp.note.strip() in frequent_note_dict:
            frequent_note_dict[eventstamp.note.strip()] += 1
        elif eventstamp.note.strip() not in depricated_notes: 
            frequent_note_dict[eventstamp.note.strip()] = 1
    most_freq_list = list()
    for key in frequent_note_dict:
        most_freq_list.append( (frequent_note_dict[key], key) )
    most_freq_list.sort()
    most_freq_list.reverse()
    note_shortcut_list = list()
    for i in range(min(number_of_note_shortcuts, len(most_freq_list))):
        note_shortcut_list.append(most_freq_list[i][1]) 
    return note_shortcut_list

def refresh_scales(minute_scale, hour_scale, day_scale, \
                   month_scale,  year_scale):
    minute_scale.set(datetime.today().minute)
    hour_scale.set(  datetime.today().hour)
    day_scale.set(   datetime.today().day)
    month_scale.set( datetime.today().month)
    year_scale.set(  datetime.today().year)

def set_scales_to_last_eventstamp(minute_scale, hour_scale, day_scale, \
                                 month_scale,   year_scale):
    eventstamp_list = eventstamp_parser.make_eventstamp_list()

    minute = eventstamp_list[-1].minute
    hour   = eventstamp_list[-1].hour
    day    = eventstamp_list[-1].day
    month  = eventstamp_list[-1].month
    year   = eventstamp_list[-1].year

    minute_scale.set(minute)
    hour_scale.set(hour)
    day_scale.set(day)
    month_scale.set(month)
    year_scale.set(year)

def update_data_files(): 
    #this is not keeping the GUI free, but its 10 times faster :/ 
    #t1 = datetime.today()
    data_parser_list = [eventstamp_txt_data_following.main, \
                        eventstamp_txt_data_by_minute.main, \
                        eventstamp_txt_data_by_day.main, \
                        eventstamp_sql_data_by_day.main ]
    for data_parser in data_parser_list:
        process = Process(target = data_parser)
        process.start()
        #process.join()
    #t2 = datetime.today()
    #print(t2-t1)
