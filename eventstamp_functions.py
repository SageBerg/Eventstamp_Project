'''
eventstamp_functions.py
this file imported by eventstamp_gui_functions.py
to map functions as callbacks for gui buttons

Sage Berg
Created 10 April 2014
Edited  01 June  2014
'''

from datetime import *
from eventstamp_variables import *
import eventstamp_parser 

def make_people_string(people_list):
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
    display_list.append(display.create_rectangle(start_x, 0, end_x, 40, fill=color, width=0))

def write_eventstamp(activity_string, people_string, happiness, note, where, stress, scales, scales_list, display, display_list):
    outfile   = open('eventstamp_data.txt', 'a')
    if scales.get():
        minute = zero_padder(scales_list[0].get())
        hour   = zero_padder(scales_list[1].get())
        day    = zero_padder(scales_list[2].get())
        month  = zero_padder(scales_list[3].get())
        year   = str(scales_list[4].get())
        timestamp = year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':00.000000'
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
    return lines[-1][5:16] + lines[-1][26:-14] #get the last line and don't include it's \n

def make_frequent_note_dict(eventstamp_list): #function needs a clean up
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
    quick_note_list = list()
    x = 56 #changes number of note buttons that appear when eventstamp.py is run
    for i in range(min(x, len(most_freq_list))): #collect x most common notes
        quick_note_list.append(most_freq_list[i][1]) 
    return quick_note_list

def refresh_scales(minute_scale, hour_scale, day_scale, month_scale, year_scale):
    minute_scale.set(datetime.today().minute)
    hour_scale.set(  datetime.today().hour)
    day_scale.set(   datetime.today().day)
    month_scale.set( datetime.today().month)
    year_scale.set(  datetime.today().year)

def set_scales_to_last_eventstamp(minute_scale, hour_scale, day_scale, month_scale, year_scale):
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
