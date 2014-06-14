'''
eventstamp_gui_functions.py
functions imported by eventstamp.py
functions draw different parts of the eventstamp.py gui

Created 10 April 2014
'''

from tkinter              import *
from datetime             import *
from eventstamp_functions import *
from eventstamp_calendar  import *
from eventstamp_parser    import *
from eventstamp_variables import *

try:
    from personal_people_list import people
except:
    print('failed to import personal_people_list')

root = Tk()
root.configure(background='white')
root.wm_title('Eventstamp.py')

people_list = [(person, IntVar()) for person in people]
location = ''
stress_bool = IntVar()
scales_bool = IntVar()

def draw_time_scales():
    can_width  = 52
    can_height = 38
    tx = 27
    ty = 30

    minute_title = Canvas(root, height=can_height, width=can_width)
    minute_title.grid(row=7, column=13, columnspan=2)
    minute_title.create_text(tx,ty, text="Minute")
    minute_scale = Scale(root, from_=0, to=59, \
                         orient=HORIZONTAL, length=221)
    minute_scale.grid(row=7, column=14, columnspan=2, padx=5)

    hour_title = Canvas(root, height=can_height, width=can_width)
    hour_title.grid(row=8, column=13, columnspan=2)
    hour_title.create_text(tx,ty, text="Hour")
    hour_scale = Scale(root, from_=0, to=23, \
                       orient=HORIZONTAL, length=221)
    hour_scale.grid(row=8, column=14, columnspan=2, padx=5)

    day_title = Canvas(root, height=can_height, width=can_width)
    day_title.grid(row=9, column=13, columnspan=2)
    day_title.create_text(tx,ty, text="Day")
    day_scale = Scale(root, from_=1, to=31, orient=HORIZONTAL, length=221)
    day_scale.grid(row=9, column=14, columnspan=2, padx=5) 

    month_title = Canvas(root, height=can_height, width=can_width)
    month_title.grid(row=10, column=13, columnspan=2)
    month_title.create_text(tx,ty, text="Month")
    month_scale = Scale(root, from_=1, to=12, \
                        orient=HORIZONTAL, length=221)
    month_scale.grid(row=10, column=14, columnspan=2, padx=5)

    year_title = Canvas(root, height=can_height, width=can_width)
    year_title.grid(row=11, column=13, columnspan=2)
    year_title.create_text(tx,ty, text="Year")
    year_scale = Scale(root, from_=2014, to=2100, \
                       orient=HORIZONTAL, length=221)
    year_scale.grid(row=11, column=14, columnspan=2, padx=5) 

    refresh_scales(minute_scale, hour_scale, day_scale, \
                   month_scale,  year_scale)

    refresh_scales_button = Button(root, height=1, width=6, \
                                   text="Current", \
    command=lambda 
    minute = minute_scale,
    hour   = hour_scale,
    day    = day_scale,
    month  = month_scale,
    year   = year_scale:
    refresh_scales(minute,hour,day,month,year), wraplength=100)
    refresh_scales_button.grid(row=8, column=13, columnspan=1, padx=5)

    set_scales_to_last_time_button = Button(root, height=1, width=6, \
                                            text="Last Time", \
    command=lambda
    minute = minute_scale,
    hour   = hour_scale,
    day    = day_scale,
    month  = month_scale,
    year   = year_scale:
    set_scales_to_last_eventstamp(minute,hour,day,month,year), \
                                  wraplength=100)
    set_scales_to_last_time_button.grid(row=9, column=13, padx=5)

    return [minute_scale, hour_scale, day_scale, month_scale, year_scale]

def draw_activity_buttons(event_list,  happiness,   note_entry_box, \
                          stress_bool, scales_bool, scales_list, \
                          display,     display_list):
    buttons_list = list() 
    i = 0
    j = 0
    for event in event_list:
        buttons_list.append(Button(root, width = 6, height = 4, \
                                   text=event[0].title(), \
                                   bg=event[1], fg=event[2], \
                                   activebackground=event[1], \
                                   activeforeground = event[2], \
                                   wraplength=70, 
        command=lambda 
        activity_string=event[0].title(), 
        p=people_list, 
        hap=happiness, 
        note=note_entry_box.get, 
        where=location,
        stress=stress_bool,
        scales=scales_bool,
        scales_list=scales_list,
        disp=display,
        disp_list=display_list
        :
        write_eventstamp(
        activity_string,
        make_people_string(p),
        hap,
        note(), 
        where,  
        stress, 
        scales,
        scales_list,
        disp,
        disp_list
        )))
 
        buttons_list[-1].grid(\
        row=j, column=i*2, columnspan=2, padx=5, pady=5)
        j += 1
        j = j%7
        if j == 0:
            i += 1

def draw_people_checkboxes(people_list):
    check_box_list = list()
    r = 7 
    k = 0
    for person in people_list:
        check_box_list.append(\
        Checkbutton(root, text=person[0].title(), variable=person[1], \
        width=6, bg='white', activebackground='white'))
        check_box_list[-1].grid(\
        row=r, column=k*2, columnspan=2, padx=5, pady=5)
        k += 1
        k = k%4
        if k == 0:
            r += 1
    return check_box_list

def draw_happiness_buttons():
    radio_button_list = list()
    happiness = IntVar() 
    for i in range(1,6):
        radio_button_list.append(Radiobutton(\
        root, text=str(i), \
        variable=happiness, \
        value=i, \
        highlightcolor='white', \
        indicatoron=0, \
        height=2, \
        width=15, \
        bg=happiness_color_dict[str(i)][0], \
        activebackground=happiness_color_dict[str(i)][0])) 
        radio_button_list[-1].grid(row=10, column=7+i)
    radio_button_list[2].select() #happiness level 3 selected by default
    return happiness

def draw_note_buttons(note_list, note_entry_box, note_entry_string):
    note_button_list = list()
    x = 0 
    y = 4 
    for note in note_list:
        note_button_list.append(Button(\
        root, text=note, width=12, height=4, bg='white', wraplength=100,
        command=lambda button_label=note, \
        change_note=note_entry_string.set: change_note(button_label)))
        note_button_list[-1].grid(row=x, column=y+4, padx=5, pady=5)
        x += 1
        x = x%7
        if x == 0:
            y += 1

def draw_note_entry_box():
    note_entry_string = StringVar()
    note_entry_box = Entry(\
    root, textvariable=note_entry_string, width=25, justify=CENTER)
    note_entry_box.grid(row=7, column=9, columnspan=3, padx=5)
    return note_entry_box, note_entry_string

def draw_stress_box(stress_bool):
    stress_box = Checkbutton(\
    root, text='Stressed', variable=stress_bool, width=12)
    stress_box.grid(row=8, column=12, columnspan=1, padx=5)

def draw_time_scales_check_box(scales_bool):
    check_box = Checkbutton(\
    root, text='Scales', width=6, variable=scales_bool)
    check_box.grid(row=7,column=13,columnspan=1,padx=5)

def draw_delete_last_stamp_button(display, display_list):
    delete_last_stamp_button = Button(root, text='Delete Last Stamp', \
    command=lambda 
    display=display,
    display_list=display_list:
    undo(display, display_list), width=12)
    delete_last_stamp_button.grid(\
    row=9, column=12, columnspan=1, padx=5, pady=5)

def draw_last_stamp_button(last_stamp_string):
    calendar_button = Button(root, text='See Last Stamp', \
    command=lambda 
    change_text=last_stamp_string.set
    : 
    change_text(get_last_stamp()), width=12)
    calendar_button.grid(row=9, column=8, padx=5, pady=5)

def draw_last_stamp_entry():
    last_stamp_string = StringVar()
    last_stamp_entry = Entry(\
    root, textvariable=last_stamp_string, width=48, justify=CENTER)
    last_stamp_entry.grid(row=9, column=9, columnspan=3, pady=5)
    return last_stamp_string

def draw_calendar_buttons():
    button_text_list = ['Activities', 'Happiness', 'People', 'Stress']
    callback_list = \
    [eventstamp_calendar, happiness_calendar, \
    people_calendar, stress_calendar]
    for i in range(4):
        calendar_button = Button(\
        root, text=button_text_list[i], width=12, \
        command=lambda x = callback_list[i]: x() )
        calendar_button.grid(row=8, column=8+i, padx=5, pady=5)

def draw_update_data_files_button():
    data_files_button = Button(root, text='Update Data Files', width=12, \
    command=lambda x = update_data_files: x() )
    data_files_button.grid(row=7, column=8, padx=5, pady=5)

def draw_realtime_eventstamp_display():
    display = Canvas(root, height=55, width=1440, bg='white')
    display.create_line(0, 40, 1440, 40, fill='grey')

    for hour in range(24):
        display.create_line(hour*60, 0, hour*60, 60, fill='grey')
        display.create_text(hour*60 + 30, 50, text=str(hour) +':00') 
        
    eventstamp_list    = make_eventstamp_list()
    display_list = list()

    for i in range(len(eventstamp_list)):
        if eventstamp_list[i].date == \
        (datetime.today().year -2000, 
         datetime.today().month, 
         datetime.today().day):
            color = 'black'
            for event in event_list: #tacky code
                if eventstamp_list[i].what.lower() == event[0]:
                    color = event[1]
            if eventstamp_list[i-1].day == eventstamp_list[i].day:
                start_x = \
                eventstamp_list[i-1].minute + eventstamp_list[i-1].hour*60
            else:
                start_x = 0
            end_x = eventstamp_list[i].minute + eventstamp_list[i].hour*60
            display_list.append(\
            display.create_rectangle(\
            start_x, 0, end_x, 40, fill=color, width=0)) 
    display.grid(row=20, columnspan=16, padx=5, pady=5)
    return display, display_list
