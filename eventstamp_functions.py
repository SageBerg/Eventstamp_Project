'''
eventstamp_functions.py
this file imported by eventstamp_gui.py
to map functions as callbacks for gui buttons

Sage Berg
Created 10 April 2014
'''

from multiprocessing      import Process 
from datetime             import *
from eventstamp_variables import *
from eventstamp_parser    import *

import eventstamp_txt_data_following 
import eventstamp_txt_data_by_minute
import eventstamp_txt_data_by_day
import eventstamp_sql_data_by_day
import eventstamp_html_blocks
import eventstamp_html_happy_blocks

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

def make_people_string(people_list): #used by draw_activity_buttons
    people_string = ''
    for person in people_list:
         if person[1].get():
            people_string += person[0] + ' '
    return people_string

def get_activity_display_color(eventstamp):
    index = inverted_event_map[eventstamp.what.strip().lower()]
    return event_list[index][1] 

def get_people_display_color(eventstamp):
    if eventstamp.who.strip() != '':
        index = inverted_event_map[eventstamp.what.strip().lower()]
        return event_list[index][1] 
    else:
        return 'white'

def get_happiness_display_color(eventstamp):
    if eventstamp.what == 'Sleep':
        return 'white'
    return happiness_color_dict[eventstamp.happiness][0]

def write_eventstamp(activity_string, people_string, happiness, 
                     note_string,     where,         stress, 
                     scales,          scales_list,   display_observer):
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
    note      = note_string.replace(',','') #no commas in input strings
    people    = people_string.replace(',','') 
    stress_string = stress

    try:
        if int(happiness) < 1:
            happiness = '1'
        if int(happiness) > 5:
            happiness = '5'
    except:
        happiness = '3' #assume neutral happiness for invalid input

    if stress.get() == 1:
        stress_string = 'stress'
    else:
        stress_string = 'no stress'
    outfile.write(timestamp + ', ' + activity_string + ', '
                + people_string + ', ' + happiness + ', ' + note 
                + ', ' + where + ', ' + stress_string + '\n')
    outfile.close() 

    display_observer.notify()

def zero_padder(n):
    '''takes int, returns string'''
    if n < 10:
        return '0' + str(n)
    return str(n)   

def add_remove_people_from_entry_box(person_entry_box, 
                                     person_string,
                                     person_entry_string):
    new_person_string = ''
    if person_string not in person_entry_box.get().split():
        new_person_string = person_entry_box.get() + ' ' + person_string
    else:
        for person in person_entry_box.get().split():
            if person != person_string:
                new_person_string += person + ' '
    person_entry_string.set(new_person_string)

def undo(realtime_display_observer): 
    #callback for "delete last stamp" button
    lines  = open('eventstamp_data.txt', 'r').readlines()
    line_cnt = 0
    for line in lines:
        line_cnt += 1
    open('eventstamp_data.txt', 'w').writelines(lines[:line_cnt-1])
    realtime_display_observer.notify()

def get_last_stamp():
    lines  = open('eventstamp_data.txt', 'r').readlines()
    return lines[-1][5:16] + lines[-1][26:-14] 
    #get the last line and don't include it's \n

def make_note_shortcut_list(eventstamp_list): 
    #function needs a clean up 
    #changes number of note buttons that appear when eventstamp.py is run
    number_of_note_shortcuts = 63 #most common non-depricated notes
    frequent_note_dict = dict()
    for eventstamp in eventstamp_list: 
        note = eventstamp.note.strip() 
        act  = eventstamp.what.strip()
        if note in frequent_note_dict:
            frequent_note_dict[note][0] += 1
            #print(frequent_note_dict[note][1])
            if act not in frequent_note_dict[note][1]:
                frequent_note_dict[note][1][act] = 1
            else:
                frequent_note_dict[note][1][act] += 1
        elif note not in depricated_notes: 
            by_activity_dict = dict()
            by_activity_dict[act] = 1
            frequent_note_dict[note] = [1, by_activity_dict] 
    most_freq_list = list()
    for key in frequent_note_dict:
        freq = frequent_note_dict[key][0]
        max_act = 0
        max_act_string = ''
        for act_key in frequent_note_dict[key][1]:
            #print(frequent_note_dict[key][1][act_key])
            if frequent_note_dict[key][1][act_key] > max_act:
                max_act = frequent_note_dict[key][1][act_key]
                max_act_string = act_key.strip()
        for event in event_list:
            if event[0] == max_act_string.lower():
                b  = event[1]
                f  = event[2]
                ab = event[3]
                af = event[2]
                break
            else:
                b  = 'white'
                f  = 'black'
                ab = 'blue'
                af = 'red'
        most_freq_list.append( (frequent_note_dict[key][0], key, b, f, ab, af) ) 
    most_freq_list.sort()
    most_freq_list.reverse()
    note_shortcut_list = list()
    for i in range(min(number_of_note_shortcuts, len(most_freq_list))):
        #append(note, background_fill, text_fill, active_background_fill)
        note_shortcut_list.append( ( most_freq_list[i][1], 
                                     most_freq_list[i][2],   
                                     most_freq_list[i][3], 
                                     most_freq_list[i][4],
                                     most_freq_list[i][5]) )
    if len(note_shortcut_list) < number_of_note_shortcuts:
        for i in range(number_of_note_shortcuts -len(note_shortcut_list)):
            note_shortcut_list.append('', 'white', 'black', 'white', 'black') 
            #for appearence of gui 
    return note_shortcut_list

def refresh_scales(minute_scale, hour_scale, day_scale, \
                   month_scale,  year_scale):
    minute_scale.set(datetime.today().minute)
    hour_scale.set(  datetime.today().hour)
    day_scale.set(   datetime.today().day)
    month_scale.set( datetime.today().month)
    year_scale.set(  datetime.today().year)

def set_scales_to_last_eventstamp(minute_scale, hour_scale, day_scale, 
                                 month_scale,   year_scale):
    #must make new eventstamp_list to have up-to-date information 
    eventstamp_list = make_eventstamp_list()

    minute = eventstamp_list[-1].minute
    hour   = eventstamp_list[-1].hour
    day    = eventstamp_list[-1].day
    month  = eventstamp_list[-1].month
    year   = eventstamp_list[-1].year

    minute_scale.set(minute)
    hour_scale.set(hour)
    day_scale.set(day)
    month_scale.set(month)
    year_scale.set(year + 2000) 
    #+2000 because eventstamp.year returns yy not yyyy e.g. 14 not 2014

def update_data_files(): 
    #this is not keeping the GUI free, but its 10 times faster :/ 
    #t1 = datetime.today()
    data_parser_list = [eventstamp_txt_data_following.main, \
                        eventstamp_txt_data_by_minute.main, \
                        eventstamp_txt_data_by_day.main, \
                        eventstamp_sql_data_by_day.main]
    for data_parser in data_parser_list:
        process = Process(target = data_parser)
        process.start()
        #process.join()
    #t2 = datetime.today()
    #print(t2-t1)
    eventstamp_html_blocks.HTML_Blocks()
    eventstamp_html_happy_blocks.HTML_Blocks()

def calculate_today_happiness():
    eventstamp_list = make_eventstamp_list()
    happiness_sum = 0
    divisor = 0
    for i in range(1, len(eventstamp_list)):
        e = ( datetime.today().year -2000, 
              datetime.today().month, 
              datetime.today().day )
        if eventstamp_list[i].date == e and \
           eventstamp_list[i].what != 'Sleep':
            duration = get_eventstamp_duration(i, eventstamp_list)
            happiness_sum += int(eventstamp_list[i].happiness)*duration
            divisor += duration
    if divisor == 0: #to avoid dividing by 0
        divisor += 1
    return round(happiness_sum/divisor, 3)

def today_people_time():
    eventstamp_list = make_eventstamp_list()
    people_minute_sum = 0
    divisor = 0
    for i in range(1, len(eventstamp_list)):
        e = ( datetime.today().year -2000, 
              datetime.today().month, 
              datetime.today().day )
        if eventstamp_list[i].date == e: 
            duration = get_eventstamp_duration(i, eventstamp_list)
            if eventstamp_list[i].who:
                people_minute_sum += duration
            divisor += duration
    if divisor == 0: #to avoid dividing by 0
        divisor += 1
    return round(people_minute_sum/divisor, 3)*100

def today_number_of_stamps():
    eventstamp_list = make_eventstamp_list()
    number_of_stamps = 0
    for i in range(1, len(eventstamp_list)):
        e = ( datetime.today().year -2000, 
              datetime.today().month, 
              datetime.today().day )
        if eventstamp_list[i].date == e:
            number_of_stamps += 1
    return number_of_stamps

def today_productivity():
    eventstamp_list = make_eventstamp_list()
    pro_minute_sum = 0
    divisor = 0
    non_productive = ['Games', 'Video', 'Audio', 
                      'Read', 'Social', 'Idle'] 
    for i in range(1, len(eventstamp_list)):
        e = ( datetime.today().year -2000, 
              datetime.today().month, 
              datetime.today().day )
        if eventstamp_list[i].date == e: 
            duration = get_eventstamp_duration(i, eventstamp_list)
            if eventstamp_list[i].what not in non_productive:
                pro_minute_sum += duration
            divisor += duration
    if divisor == 0: #to avoid dividing by 0
        divisor += 1
    return round(pro_minute_sum/divisor, 3)*100
