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
    scale_length = 220
    can_width  = 72 
    can_height = 34
    tx = 36
    ty = 28 
    
    base_row   = 12
    base_col   = 0
    col_mod    = 2
    col_span   = 6

    minute_title = Canvas(root, height=can_height, width=can_width,
                        )
    minute_title.grid(row=base_row, column=base_col, columnspan=2)
    minute_title.create_text(tx,ty, text="Minute")
    minute_scale = Scale(root, from_=0, to=59, 
                         orient=HORIZONTAL, length=scale_length,
                         sliderrelief=FLAT, troughcolor='gray50', 
                         bd=0)
    minute_scale.grid(row=base_row, 
                      column=base_col+col_mod, 
                      columnspan=col_span)

    hour_title = Canvas(root, height=can_height, width=can_width,
                        )
    hour_title.grid(row=base_row+1, column=base_col, columnspan=2)
    hour_title.create_text(tx,ty, text="Hour")
    hour_scale = Scale(root, from_=0, to=23, 
                       orient=HORIZONTAL, length=scale_length,
                         sliderrelief=FLAT, troughcolor='gray50', 
                         bd=0, )
    hour_scale.grid(row=base_row+1, 
                    column=base_col+col_mod, 
                    columnspan=col_span)

    day_title = Canvas(root, height=can_height, width=can_width,
                        )
    day_title.grid(row=base_row+2, column=base_col, columnspan=2)
    day_title.create_text(tx,ty, text="Day")
    day_scale = Scale(root, from_=1, to=31, orient=HORIZONTAL, 
                         length=scale_length,
                         sliderrelief=FLAT, troughcolor='gray50', 
                         bd=0, )
    day_scale.grid(row=base_row+2, 
                   column=col_mod, 
                   columnspan=col_span) 

    month_title = Canvas(root, height=can_height, width=can_width,
                        )
    month_title.grid(row=base_row+3, column=base_col, columnspan=2)
    month_title.create_text(tx,ty, text="Month")
    month_scale = Scale(root, from_=1, to=12, \
                        orient=HORIZONTAL, length=scale_length,
                        sliderrelief=FLAT, troughcolor='gray50', 
                        bd=0, )
    month_scale.grid(row=base_row+3, 
                     column=base_col+col_mod, 
                     columnspan=col_span)

    year_title = Canvas(root, height=can_height, width=can_width, 
                        )
    year_title.grid(row=base_row+4, column=base_col, columnspan=2)
    year_title.create_text(tx,ty, text="Year")
    year_scale = Scale(root, from_=2000, to=2099, \
                       orient=HORIZONTAL, length=scale_length,
                       sliderrelief=FLAT, troughcolor='gray50', 
                       bd=0, )
    year_scale.grid(row=base_row+4, 
                    column=base_col+col_mod, 
                    columnspan=col_span) 

    refresh_scales(minute_scale, hour_scale, day_scale, \
                   month_scale,  year_scale)

    refresh_scales_button = Button(root, height=1, width=6, 
                                   text="Current",
                                   relief=FLAT,
    command=lambda 
    minute = minute_scale,
    hour   = hour_scale,
    day    = day_scale,
    month  = month_scale,
    year   = year_scale:
    refresh_scales(minute,hour,day,month,year), wraplength=100)
    refresh_scales_button.grid(row=12, column=9)

    set_scales_to_last_time_button = Button(root, height=1, width=6, 
                                            text="Last Time", 
                                            relief=FLAT,
    command=lambda
    minute = minute_scale,
    hour   = hour_scale,
    day    = day_scale,
    month  = month_scale,
    year   = year_scale:
    set_scales_to_last_eventstamp(minute,hour,day,month,year), 
                                  wraplength=100)
    set_scales_to_last_time_button.grid(row=13, column=9)

    return [minute_scale, hour_scale, day_scale, month_scale, year_scale]

def draw_activity_buttons(event_list,  happiness,   note_entry_box, 
                          stress_bool, scales_bool, scales_list, 
                          display,     display_list):
    buttons_list = list() 
    i = 0
    j = 0
    for event in event_list:
        buttons_list.append(Button(root, width = 6, height = 4, 
                                   text=event[0].title(), 
                                   bg=event[1], fg=event[2], 
                                   activebackground=event[3], 
                                   activeforeground=event[2], 
                                   wraplength=70, 
                                   relief=FLAT,
                                   bd=0,
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
        row=j, column=i*2, columnspan=2,  )
        j += 1
        j = j%7
        if j == 0:
            i += 1

def draw_people_checkboxes(people_list):
    check_box_list = list()
    r = 9 
    k = 9 
    for person in people_list:
        check_box_list.append(\
        Checkbutton(root, text=person[0].title(), variable=person[1], \
        width=6, height=4, bg='white', activebackground='white'))
        check_box_list[-1].grid(\
        row=r, column=k)
        k += 1
    return check_box_list

def draw_people_buttons(people_list, people_entry_box, people_entry_string):
    people_button_list = list()
    x = 0
    y = 7
    for i in range(len(people_list)):
        people_button_list.append(
        Button(root, text=people_list[i][0].title(),
        width=6, height=4, bg='white', wraplength=100, bd=0, 
        command=lambda button_label=people_list[i], 
        change_note=people_entry_string.set: change_note(button_label)))
        people_button_list[-1].grid(row=y, column=x*2, columnspan=2)
        x += 1
        x =  x%4
        if x == 0:
            y += 1 

def draw_happiness_buttons():
    radio_button_list = list()
    happiness = IntVar() 
    for i in range(1,6):
        radio_button_list.append(Radiobutton(
        root, text=str(i), 
        variable=happiness, 
        value=i, 
        highlightcolor='white', 
        indicatoron=0, 
        height=1, 
        width=2,
        relief=FLAT,
        bg=happiness_color_dict[str(i)][0], \
        activebackground=happiness_color_dict[str(i)][0])) 
        radio_button_list[-1].grid(row=10, column=i+1)
    radio_button_list[2].select() #happiness level 3 selected by default
    return happiness

def X_draw_happiness_buttons():
    for i in range(1,6):
        button = Button(root, text=str(i), width=12, height=4, bd=0,
                        relief=FLAT, bg=happiness_color_dict[str(i)][0],
                        fg=happiness_color_dict[str(i)][1])
        button.grid(row=1+i, column=18) 

def draw_note_buttons(note_list, note_entry_box, note_entry_string):
    note_button_list = list()
    x = 0 
    y = 4 
    for note in note_list:
        note_button_list.append(Button(
        root, text=note, width=12, height=4, bg='white', wraplength=100,
        bd=0, 
        command=lambda button_label=note, 
        change_note=note_entry_string.set: change_note(button_label)))
        note_button_list[-1].grid(row=x, column=y+5)
        x += 1
        x = x%7
        if x == 0:
            y += 1

def draw_entry_box_canvas():
    entry_box_canvas = Canvas(root, width=1096, height=142, bg='#ffffff')
    entry_box_canvas.grid(row=7, column=8, rowspan=2, columnspan=10)
    text_list = ['Note to include in next eventstamp', 
                 'Add note button',          
                 'Remove note button',       
                 'People to include in next eventstamp',
                 'Add person button',
                 'Remove person button',
                 ]
    x = 185 
    y = 13
    for title in text_list:
        if x >= 1030:
           x = 185 
           y += 66
        entry_box_canvas.create_text(x, y, text=title)
        x += 365

def draw_note_entry_box():
    note_entry_string = StringVar()
    note_entry_box = Entry(
    root, textvariable=note_entry_string, width=25, justify=CENTER,
    relief=FLAT)
    note_entry_box.grid(row=7, column=9, columnspan=3)
    return note_entry_box, note_entry_string

def draw_people_entry_box():
    people_entry_string = StringVar()
    people_entry_box = Entry(
    root, textvariable=people_entry_string, width=25, justify=CENTER,
    relief=FLAT)
    people_entry_box.grid(row=8, column=9, columnspan=3)
    return people_entry_box, people_entry_string

def draw_add_note_shortcut_entry_box():
    shortcut_string = StringVar()
    shortcut_entry_box = Entry(
    root, textvariable=shortcut_string, width=25, justify=CENTER,
    relief=FLAT)
    shortcut_entry_box.grid(row=7, column=12, columnspan=3)
    return shortcut_entry_box, shortcut_string

def draw_add_people_shortcut_entry_box():
    shortcut_string = StringVar()
    shortcut_entry_box = Entry(
    root, textvariable=shortcut_string, width=25, justify=CENTER,
    relief=FLAT)
    shortcut_entry_box.grid(row=8, column=12, columnspan=3)
    return shortcut_entry_box, shortcut_string

def draw_remove_note_shortcut_entry_box():
    shortcut_string = StringVar()
    shortcut_entry_box = Entry(
    root, textvariable=shortcut_string, width=25, justify=CENTER,
    relief=FLAT)
    shortcut_entry_box.grid(row=7, column=15, columnspan=3)
    return shortcut_entry_box, shortcut_string

def draw_remove_people_shortcut_entry_box():
    shortcut_string = StringVar()
    shortcut_entry_box = Entry(
    root, textvariable=shortcut_string, width=25, justify=CENTER,
    relief=FLAT)
    shortcut_entry_box.grid(row=8, column=15, columnspan=3)
    return shortcut_entry_box, shortcut_string

def draw_stress_box(stress_bool):
    stress_box = Checkbutton(
    root, text='Stress', variable=stress_bool, width=6)
    stress_box.grid(row=10, column=0)

def draw_time_scales_check_box(scales_bool):
    check_box = Checkbutton(\
    root, text='Scales', width=6, variable=scales_bool)
    check_box.grid(row=11, column=0)

def draw_delete_last_stamp_button(display, display_list):
    delete_last_stamp_button = Button(root, text='Delete Last Stamp', 
    relief=FLAT, bd=0,
    command=lambda 
    display=display,
    display_list=display_list:
    undo(display, display_list), height=4, width=12)
    delete_last_stamp_button.grid(
    row=1, column=18)

def draw_last_stamp_button(last_stamp_string):
    calendar_button = Button(root, text='See Last Stamp', \
    relief=FLAT,
    command=lambda 
    change_text=last_stamp_string.set
    : 
    change_text(get_last_stamp()), width=12)
    calendar_button.grid(row=9, column=18 )

def draw_last_stamp_entry():
    last_stamp_string = StringVar()
    last_stamp_entry = Entry(\
    root, textvariable=last_stamp_string, width=48, justify=CENTER, 
    relief=FLAT)
    last_stamp_entry.grid(row=9, column=19, columnspan=3, )
    return last_stamp_string

def draw_calendar_buttons():
    button_text_list = ['Activities Calendar', 'Happiness Calendar', 
                        'People Calendar']
    callback_list = [eventstamp_calendar, happiness_calendar, 
                     people_calendar]
    for i in range(len(button_text_list)):
        calendar_button = Button(
        root, text=button_text_list[i], width=12, height=4,
        relief=FLAT, bd=0, wraplength=70,
        command=lambda x = callback_list[i]: x() )
        calendar_button.grid(row=7+i, column=18)

def draw_update_data_files_button():
    data_files_button = Button(root, text='Update Data Files', width=12, 
    height=4, relief=FLAT, bd=0, 
    command=lambda x = update_data_files: x() )
    data_files_button.grid(row=0, column=18)

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
            display_list.append(
            display.create_rectangle(
            start_x, 0, end_x, 40, fill=color, width=0)) 
    display.grid(row=20, columnspan=19)
    return display, display_list
