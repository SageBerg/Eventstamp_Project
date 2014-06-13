'''
eventstamp_parser.py

Sage Berg
Created: 04 March 2014
'''

from eventstamp_class import Eventstamp 

def parse_datetime_string(datetime_string):
    '''
    takes in a datetime string
    returns the year, month, day, hour, and minute in a list 
    '''
    year   = int(datetime_string[2] + datetime_string[3])
    month  = int(datetime_string[5] + datetime_string[6])
    day    = int(datetime_string[8] + datetime_string[9])
    hour   = int(datetime_string[11] + datetime_string[12])
    minute = int(datetime_string[14] + datetime_string[15])
    return (year, month, day, hour, minute)

def get_date(datetime_string):
    '''
    '''
    year   = int(datetime_string[2] + datetime_string[3])
    month  = int(datetime_string[5] + datetime_string[6])
    day    = int(datetime_string[8] + datetime_string[9])
    return (year, month, day) 

def make_eventstamp_list(): 
    '''
    returns list of eventstamp ojects
    '''
    eventstamp_file = open('eventstamp_data.txt')
    eventstamp_list = list() 
    eventstamp_string_list = [line for line in eventstamp_file]
    for i in range(1,len(eventstamp_string_list)):
        date_of_previous_activity = get_date(eventstamp_string_list[i-1])
        date_of_current_activity  = get_date(eventstamp_string_list[i])

        line = eventstamp_string_list[i] 
        parts_list = list(parse_datetime_string(line.split(',')[0])) + line.split(',')[1:]
        for i in range(len(parts_list)): #clean up data
            if type(parts_list[i]) == str:
                parts_list[i] = parts_list[i].strip()
        if date_of_current_activity == date_of_previous_activity:
            eventstamp_list.append(Eventstamp(*parts_list))
        else: #break up events that span from one day to the next
            before_midnight_args = list(date_of_previous_activity) + [23] + [60] + parts_list[5:]
            after_midnight_args  = list(date_of_current_activity) + parts_list[3:] 
            eventstamp_list.append(Eventstamp(*before_midnight_args))
            eventstamp_list.append(Eventstamp(*after_midnight_args))
    eventstamp_file.close()
    return eventstamp_list

def make_recent_date_dict(): #refactor using eventstamp.date logic?
    '''
    '''
    date_dict = dict()
    date_set = set()
    eventstamp_file = open('eventstamp_data.txt')
    eventstamp_string_list = [line for line in eventstamp_file] 
    eventstamp_file.close()
    for i in range(len(eventstamp_string_list)):
        date_tuple = get_date(eventstamp_string_list[i]) 
        date = date_tuple[:3]
        date_set.add(date)
    date_list = list(date_set)
    date_list.sort()
    date_list.reverse()
    date_dict = {i:date_list[6-i] for i in range(7)}
    return date_dict

def make_date_dict():
    date_dict = dict()
    date_set = set()
    eventstamp_file = open('eventstamp_data.txt')
    eventstamp_string_list = [line for line in eventstamp_file] 
    eventstamp_file.close()
    for i in range(len(eventstamp_string_list)):
        date_tuple = get_date(eventstamp_string_list[i]) 
        date = date_tuple[:3]
        date_set.add(date)
    date_list = list(date_set)
    date_list.sort()
    date_dict = {i:date_list[i] for i in range(len(date_list))}
    return date_dict
