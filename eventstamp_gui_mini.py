'''
eventstamp_gui_mini.py
draw an interface that can fit on non-hi-def screens
functions imported by eventstamp.py
functions draw different parts of the eventstamp.py gui

Created 28 July 2014
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
root.wm_title('Eventstamp_Mini.py')

people_list = [(person, IntVar()) for person in people]
location = ''
stress_bool       = IntVar()

class Scales_Bool(object):

    def __init__(self):
        self.boolean = False
    def get(self):
        return self.boolean

END_SCALES_BOOL   = Scales_Bool() 
START_SCALES_BOOL = Scales_Bool()

H = 5
W = 17

def draw_scales_label_canvas(r, c, label):
    canvas = Canvas(root, height=34, width=242, bd=0)
    canvas.grid(row=r, column=c, columnspan=2)
    canvas.create_text(121, 17, text=label)

def draw_scales_time_canvas(r, c):
    canvas = Canvas(root, height=214, width=120, bd=0)
    canvas.grid(row=r, column=c, rowspan=6)
    label_list = ['minute', 'hour', 'day', 'month', 'year']
    x = 96
    y = 64
    for i in range(len(label_list)):
        canvas.create_text(x, y, text=label_list[i].title())
        y += 36 

def draw_time_scales(r, c, function):
    scale_length = 242
    span_list   = [(0,59), (0,23), (1,31), (1,12), (2000,2099)]
    scales_list = list()
    for i in range(len(span_list)):
        scales_list.append(Scale(root, from_=span_list[i][0],
                                       to   =span_list[i][1], 
                                       length=scale_length,
                                       orient=HORIZONTAL,
                                       relief=FLAT,
                                       troughcolor='gray75',
                                       bd=0,
                                       sliderrelief=FLAT) )
        scales_list[-1].grid(row=r+i, column=c, columnspan=2)
    function(*scales_list)
    return scales_list

def draw_scales_button(function, scales_list, button_text, r, c):
    button = Button(root, height=H, width=W, text=button_text,
                    relief=FLAT,    bd=0,     wraplength=100,
                    command=lambda
                    minute = scales_list[0],
                    hour   = scales_list[1],
                    day    = scales_list[2], 
                    month  = scales_list[3],
                    year   = scales_list[4]:
                    function(minute, hour, day, month, year))
    button.grid(row=r, column=c, rowspan=2)

def select_deselect(button, scales_bool):
    if scales_bool.get() == False:
        button.config(bg='#d9d9d9', fg='black', 
        activebackground='#ececec', 
        activeforeground='black')
    else:
        button.config(bg='black', fg='white', 
        activebackground='black', 
        activeforeground='white')

def multifunction(sel_desel, button, scales_bool, scales_list):
    if scales_bool.boolean:
        scales_bool.boolean = False
        for scale in scales_list:
            scale.configure(troughcolor='gray75')
    else:
        scales_bool.boolean = True
        for scale in scales_list:
            scale.configure(troughcolor='#000000')
    sel_desel(button, scales_bool)

def draw_time_scales_check_box(scales_bool, r, c, label_text, scales_list):
    check_button = Button(
    root, 
    height=H,
    width=W,
    bd=0,
    text=label_text, 
    relief =FLAT,
    wraplength=100, 
    command=lambda :
    multifunction(select_deselect, check_button, scales_bool, scales_list) )
    check_button.grid(row=r, column=c, rowspan=2)

def draw_entry_canvas(r, c):
    entry_box_canvas = Canvas(root, width=1122, height=70, bg='#ffffff')
    entry_box_canvas.grid(row=r, column=c, rowspan=2, columnspan=9) 
    text_list = ['People to include in next eventstamp',
                 'Note to include in next eventstamp', 
                 'Happiness level for next eventstamp' 
                 ]
    x = 185 
    y = 16
    for title in text_list:
        entry_box_canvas.create_text(x, y, text=title)
        x += 365

def draw_people_entry_box(r, c):
    people_entry_string = StringVar()
    people_entry_box = Entry(
    root, textvariable=people_entry_string, width=25, justify=CENTER,
    relief=FLAT)
    people_entry_box.grid(row=r, column=c, rowspan=2, columnspan=3)
    return people_entry_box, people_entry_string

def draw_note_entry_box(r, c):
    note_entry_string = StringVar()
    note_entry_box = Entry(
    root, textvariable=note_entry_string, width=25, justify=CENTER,
    relief=FLAT)
    note_entry_box.grid(row=r, column=c, rowspan=2, columnspan=3)
    return note_entry_box, note_entry_string

def draw_happiness_entry_box(r, c):
    happiness_entry_string = StringVar()
    happiness_entry_box = Entry(root, width=25,
                                relief=FLAT,
                                justify=CENTER,
                                textvariable=happiness_entry_string)
    happiness_entry_box.grid(row=r, column=c, rowspan=2, columnspan=3)
    happiness_entry_string.set('3')
    return happiness_entry_box, happiness_entry_string

def draw_people_buttons(people_list, 
                        people_entry_box, 
                        people_entry_string):
    people_button_list = list()
    x = 0
    y = 6 
    for i in range(len(people_list[:-4])):
        people_button_list.append(
        Button(root, text=people_list[i].title(),
        width=W, height=H, bg='white', wraplength=70, bd=0, 
        command=lambda 
        button_label=people_list[i], 
        f=add_remove_people_from_entry_box
        : 
        f(people_entry_box, button_label, people_entry_string))) 
        people_button_list[-1].grid(row=y,     column=x, 
                                    rowspan=1, columnspan=1)
        x += 1
        x =  x%4
        if x == 0:
            y += 2 

def draw_activity_buttons(people_ent_box, note_ent_box, hap_ent_box,
                          stress_bool,    END_SCALES_BOOL,  scales_list,
                          observer):
    buttons_list = list() 
    i = 4 
    j = 0
    for event in event_list:
        buttons_list.append(Button(root, width=W, height=H, 
                                   text=event[0].title(), 
                                   bg=event[1], fg=event[2], 
                                   activebackground=event[3], 
                                   activeforeground=event[2], 
                                   wraplength=70, 
                                   relief=FLAT,
                                   bd=0,
        command=lambda 
        activity_string=event[0].title(), 
        get_people  = people_ent_box.get,
        get_happy   = hap_ent_box.get,
        get_note    = note_ent_box.get, 
        where       = location,
        stress      = stress_bool,
        scales      = END_SCALES_BOOL,
        scales_list = scales_list,
        disp_ob     = observer
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
        disp_ob
        )))
 
        buttons_list[-1].grid(
        row=j*2, column=i, rowspan=2, columnspan=1,  )
        j += 1
        j = j%7
        if j == 0:
            i += 1

def draw_happiness_buttons(r, c, hap_entry_box, hap_entry_string):
    for i in range(1,6):
        button = Button(root, text=str(i), width=W, height=H, bd=0,
                        relief=FLAT, 
                        bg=happiness_color_dict[str(i)][0],
                        fg=happiness_color_dict[str(i)][1],
                        activebackground=happiness_color_dict[str(i)][2],
                        activeforeground=happiness_color_dict[str(i)][1],
                        command    = lambda 
                        button_hap = str(i),
                        set_hap    = hap_entry_string.set
                        :
                        set_hap(button_hap))
        button.grid(row=r+i*2, column=c, rowspan=2) 

def draw_delete_last_stamp_button(r, c, observer):
    delete_last_stamp_button = Button(root, text='Delete Last Stamp', 
    relief=FLAT, bd=0,
    command=lambda 
    realtime_display_observer=observer:
    undo(realtime_display_observer), height=H, width=W)
    delete_last_stamp_button.grid(row=r, column=c, rowspan=2)

def draw_undo_delete_last_stamp_button(display, display_list):
    delete_last_stamp_button = Button(root, text='Undo Deletion', 
    relief=FLAT, bd=0,
    height=H, width=W)
    delete_last_stamp_button.grid(
    row=9, column=18, rowspan=2)

def draw_calendar_buttons(r, c):
    button_text_list = ['Activities Calendar', 'People Calendar', 
                        'Happiness Calendar']
    callback_list = [eventstamp_calendar, people_calendar, 
                     happiness_calendar]
    for i in range(len(button_text_list)):
        calendar_button = Button(
        root, text=button_text_list[i], width=W, height=H,
        relief=FLAT, bd=0, wraplength=70,
        command=lambda x = callback_list[i]: x() )
        calendar_button.grid(row=r, column=c+i, rowspan=2)

def draw_update_data_files_button(r, c):
    data_files_button = Button(root, text='Update Data Files', width=W, 
    height=H, relief=FLAT, bd=0, 
    command=lambda x = update_data_files: x() )
    data_files_button.grid(row=r, column=c, rowspan=2)

def draw_realtime_eventstamp_display(fill_function, r, c, eventstamp_list):
    display = Canvas(root, height=70, width=1440, bg='white')
    display.create_line(0, 46, 1441, 46, fill='grey')
    for hour in range(24):
        display.create_line(hour*60, 0, hour*60, 71, fill='grey')
        #for fifteen_minute_block in range(0,60,15):
        #    display.create_line(hour*60 + fifteen_minute_block, 0, \
        #                        hour*60 + fifteen_minute_block, 51, \
        #                        fill='grey')
        display.create_text(hour*60 + 30, 59, text=str(hour) +':00') 
    display_list = list()
    for i in range(len(eventstamp_list)):
        if eventstamp_list[i].date == date_tup():
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

def draw_today_stats_canvas(eventstamp_list):
    happiness_today = 0
    ts = Today_Stats()
    hap, peeps, stamps, pro = ts.update(eventstamp_list)

    stats_canvas = Canvas(root, height=286, width=120, bg='#FFFFFF')
    stats_canvas.grid(row=7, column=18, rowspan=8)

    stats_canvas.create_text(60, 23, text = 'Activities') 
    stats_canvas.create_text(60, 46, text = str(stamps ))

    stats_canvas.create_text(60, 93, text = 'Happiness') 
    stats_canvas.create_text(60, 116, text = str(hap ) )

    people_list = str(peeps ).split('.')
    people_text = people_list[0] + '.' + people_list[1][0] + '%'
    stats_canvas.create_text(60, 166,  text = 'Time with People') 
    stats_canvas.create_text(60, 189, text = people_text) 

    productivity_list = str(pro ).split('.')
    productivity_text = productivity_list[0] + '.' + productivity_list[1][0] + '%'
    stats_canvas.create_text(60, 233, text = 'Productivity') 
    stats_canvas.create_text(60, 256, text = productivity_text) 

    return stats_canvas 
