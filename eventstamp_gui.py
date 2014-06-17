'''
eventstamp_gui.py
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

def draw_end_time_scales_canvas():
    c = Canvas(root, height=34, width=242, bd=0)
    c.grid(row=9, column=16, columnspan=2)
    c.create_text(121, 17, text='End Time Scales')

def draw_end_time_scale_label_canvas():
    c = Canvas(root, height=214, width=120, bd=0)
    c.grid(row=9, column=15, rowspan=6)
    label_list = ['minute', 'hour', 'day', 'month', 'year']
    x = 96
    y = 64
    for i in range(len(label_list)):
        c.create_text(x, y, text=label_list[i].title())
        y += 36 

def draw_scales_button(function, scales_list, button_text, r, c):
    button = Button(root, height=4, width=12, text=button_text,
                    relief=FLAT,    bd=0,     wraplength=100,
                    command=lambda
                    minute = scales_list[0],
                    hour   = scales_list[1],
                    day    = scales_list[2], 
                    month  = scales_list[3],
                    year   = scales_list[4]:
                    function(minute, hour, day, month, year))
    button.grid(row=r, column=c, rowspan=2)

def draw_time_scales():
    scale_length = 242
    tx = 36
    ty = 28 
    span_list   = [(0,59), (0,23), (1,31), (1,12), (2000,2099)]
    scales_list = list()
    for i in range(len(span_list)):
        scales_list.append(Scale(root, from_=span_list[i][0],
                                       to   =span_list[i][1], 
                                       length=scale_length,
                                       orient=HORIZONTAL,
                                       relief=FLAT,
                                       troughcolor='gray75',
                                       bd=0))
        scales_list[-1].grid(row=10+i, column=16, columnspan=2)
    refresh_scales(*scales_list)
    return scales_list

def draw_activity_buttons(event_list,  hap_ent_box,  note_entry_box, 
                          stress_bool, scales_bool,  scales_list, 
                          display,     display_list, people_entry_box):
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
        get_people  = people_entry_box.get,
        get_happy   = hap_ent_box.get,
        get_note    = note_entry_box.get, 
        where       = location,
        stress      = stress_bool,
        scales      = scales_bool,
        scales_list = scales_list,
        disp        = display,
        disp_list   = display_list
        :
        write_eventstamp(
        activity_string,
        get_people(),
        get_happy(),
        get_note(), 
        where,  
        stress, 
        scales,
        scales_list,
        disp,
        disp_list
        )))
 
        buttons_list[-1].grid(
        row=j, column=i*2, columnspan=2,  )
        j += 1
        j = j%7
        if j == 0:
            i += 1

def draw_people_buttons(people_list, 
                        people_entry_box, 
                        people_entry_string):
    people_button_list = list()
    x = 0
    y = 7
    for i in range(len(people_list)):
        people_button_list.append(
        Button(root, text=people_list[i][0].title(),
        width=6, height=4, bg='white', wraplength=100, bd=0, 
        command=lambda 
        button_label=people_list[i][0], #clean up later
        f=add_remove_people_from_entry_box
        : 
        f(people_entry_box, button_label, people_entry_string))) 
        people_button_list[-1].grid(row=y,     column=x*2, 
                                    rowspan=2, columnspan=2)
        x += 1
        x =  x%4
        if x == 0:
            y += 2 
    for i in range(16 - len(people_list)):
        people_button_list.append(
        Button(root, width=6, height=4, bg='white', bd=0))
        people_button_list[-1].grid(row=y,     column=2*x, 
                                    rowspan=2, columnspan=2)
        x += 1
        x =  x%4
        if x == 0:
            y += 2 

def draw_happiness_buttons(hap_entry_box, hap_entry_string):
    for i in range(1,6):
        button = Button(root, text=str(i), width=12, height=4, bd=0,
                        relief=FLAT, 
                        bg=happiness_color_dict[str(i)][0],
                        fg=happiness_color_dict[str(i)][1],
                        command    = lambda 
                        button_hap = str(i),
                        set_hap    = hap_entry_string.set
                        :
                        set_hap(button_hap))
        button.grid(row=1+i, column=18) 

def draw_note_buttons(note_list, note_entry_box, note_entry_string):
    note_button_list = list()
    x = 9 
    y = 0 
    for note in note_list:
        note_button_list.append(Button(
        root, text=note, width=12, height=4, bg='white', wraplength=100,
        bd=0, 
        command=lambda button_label=note, 
        change_note=note_entry_string.set: change_note(button_label)))
        note_button_list[-1].grid(row=y, column=x)
        x += 1
        x = x%18
        if x == 0:
            x += 9 
            y += 1

def draw_entry_box_canvas():
    entry_box_canvas = Canvas(root, width=1096, height=70, bg='#ffffff')
    entry_box_canvas.grid(row=7, column=8, rowspan=2, columnspan=10)
    text_list = ['Person(s) to include in next eventstamp',
                 'Note to include in next eventstamp', 
                 'Happiness level for next eventstamp' 
                 ]
    x = 185 
    y = 16
    for title in text_list:
        entry_box_canvas.create_text(x, y, text=title)
        x += 365

def draw_people_entry_box():
    people_entry_string = StringVar()
    people_entry_box = Entry(
    root, textvariable=people_entry_string, width=25, justify=CENTER,
    relief=FLAT)
    people_entry_box.grid(row=7, column=9, rowspan=2, columnspan=3)
    return people_entry_box, people_entry_string

def draw_note_entry_box():
    note_entry_string = StringVar()
    note_entry_box = Entry(
    root, textvariable=note_entry_string, width=25, justify=CENTER,
    relief=FLAT)
    note_entry_box.grid(row=7, column=12, rowspan=2, columnspan=3)
    return note_entry_box, note_entry_string

def draw_happiness_entry_box():
    happiness_entry_string = StringVar()
    happiness_entry_box = Entry(root, width=25,
                                relief=FLAT,
                                justify=CENTER,
                                textvariable=happiness_entry_string)
    happiness_entry_box.grid(row=7, column=15, rowspan=2, columnspan=3)
    happiness_entry_string.set('3')
    return happiness_entry_box, happiness_entry_string

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

def draw_happiness_entry_canvas():
    c = Canvas(root, width=120, height=70, bg='#ffffff')
    c.grid(row=1, column=18)
    c.create_text(60, 16, text='Happiness') 
    c.create_text(60, 52, text='Level') 

def draw_stress_box(stress_bool):
    stress_box = Checkbutton(
    root, text='Stress', variable=stress_bool, width=6)
    stress_box.grid(row=10, column=0)

def draw_time_scales_check_box(scales_bool):
    check_box = Checkbutton(
    root, text='Use End Scales', 
    #height=4, width=12, 
    indicatoron=False,
    offrelief=FLAT,
    relief =FLAT,
    #highlightcolor='#d9d9d9',
    variable=scales_bool,
    wraplength=100)
    check_box.grid(row=9, column=15)

def draw_delete_last_stamp_button(display, display_list):
    delete_last_stamp_button = Button(root, text='Delete Last Stamp', 
    relief=FLAT, bd=0,
    command=lambda 
    display=display,
    display_list=display_list:
    undo(display, display_list), height=4, width=12)
    delete_last_stamp_button.grid(
    row=7, column=18, rowspan=2)

def draw_undo_delete_last_stamp_button(display, display_list):
    delete_last_stamp_button = Button(root, text='Undo Deletion', 
    relief=FLAT, bd=0,
    height=4, width=12)
    delete_last_stamp_button.grid(
    row=9, column=18, rowspan=2)

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
    button_text_list = ['Activities Calendar', 'People Calendar', 
                        'Happiness Calendar']
    callback_list = [eventstamp_calendar, people_calendar, 
                     happiness_calendar]
    for i in range(len(button_text_list)):
        calendar_button = Button(
        root, text=button_text_list[i], width=6, height=4,
        relief=FLAT, bd=0, wraplength=70,
        command=lambda x = callback_list[i]: x() )
        calendar_button.grid(row=18+i, column=0, columnspan=2)

def draw_update_data_files_button():
    data_files_button = Button(root, text='Update Data Files', width=12, 
    height=4, relief=FLAT, bd=0, 
    command=lambda x = update_data_files: x() )
    data_files_button.grid(row=0, column=18)

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

def draw_realtime_eventstamp_display(fill_function, r, c):
    display = Canvas(root, height=70, width=1440, bg='white')
    display.create_line(0, 46, 1441, 46, fill='grey')
    for hour in range(24):
        display.create_line(hour*60, 0, hour*60, 71, fill='grey')
        display.create_text(hour*60 + 30, 59, text=str(hour) +':00') 
    eventstamp_list    = make_eventstamp_list()
    display_list = list()
    for i in range(len(eventstamp_list)):
        if eventstamp_list[i].date == \
        (datetime.today().year -2000, 
         datetime.today().month, 
         datetime.today().day):
            color = fill_function(eventstamp_list[i])
            if eventstamp_list[i-1].day == eventstamp_list[i].day: #coords
                start_x = \
                eventstamp_list[i-1].minute + eventstamp_list[i-1].hour*60
            else:
                start_x = 0
            end_x = eventstamp_list[i].minute + eventstamp_list[i].hour*60
            display_list.append(
            display.create_rectangle(
            start_x, 0, end_x, 46, fill=color, width=0)) 

    display.grid(row=r, column=c, columnspan=18)
    return display, display_list
