'''
eventstamp.py 
provides a GUI for keeping track of personal activities, 
social interactions, and levels of happiness

Sage Berg
Created 04 March 2014
'''

try:
    ppl = open('personal_people_list.py', 'r')
    pdn = open('personal_depricated_notes.py', 'r')
except:
    ppl = open('personal_people_list.py', 'w')
    ppl.write('#used to create people check boxes so you can record' + \
              'who you do things with\npeople = []')
    pdn = open('personal_depricated_notes.py', 'w')
    pdn.write('#notes in this list will not appear as shortcuts in' + \
              'the eventstamp.py UI\ndepricated_notes = []')
ppl.close()
pdn.close()

from eventstamp_gui import *
from eventstamp_realtime_display_class import *

def main():
    eventstamp_list           = make_eventstamp_list()
    note_shortcut_list        = make_note_shortcut_list(eventstamp_list)

    realtime_display_observer = Realtime_Display()
    realtime_display_observer.notify() #the initial draw

    draw_entry_box_canvas()
    note_entry_box,   note_entry_string = draw_note_entry_box()
    people_entry_box, people_string     = draw_people_entry_box()
    hap_entry, hap_string               = draw_happiness_entry_box()

    draw_scales_time_canvas (9, 9)
    draw_scales_label_canvas(9, 10, 'Start Time Scales')
    draw_scales_time_canvas (9, 15)
    draw_scales_label_canvas(9, 16, 'End Time Scales')
    start_scales_list = draw_time_scales(10,10, 
                                         set_scales_to_last_eventstamp)
    scales_list       = draw_time_scales(10,16, 
                                         refresh_scales)
    draw_time_scales_check_box(START_SCALES_BOOL, 9, 9, 'Use Start Scales')
    draw_time_scales_check_box(END_SCALES_BOOL,   9, 15, 'Use End Scales') 
    draw_scales_button(refresh_scales, scales_list, 
                       'Set End Scales to current time',
                       11, 14)
    draw_scales_button(set_scales_to_last_eventstamp, scales_list,
                       'Set End Scales to end time of last eventstamp',
                       13, 14)
    draw_scales_button(refresh_scales, start_scales_list, 
                       'Set Start Scales to current time',
                       11, 12)
    draw_scales_button(set_scales_to_last_eventstamp, start_scales_list,
                       'Set Start Scales to end time of last eventstamp',
                       13, 12)
    
    draw_happiness_buttons(hap_entry, hap_string)
    draw_people_buttons(people_list, people_entry_box, people_string)
    draw_activity_buttons(people_entry_box, note_entry_box, hap_entry,
                          stress_bool,      END_SCALES_BOOL,    scales_list,
                          realtime_display_observer)

    draw_calendar_buttons()
    draw_delete_last_stamp_button(realtime_display_observer)
    #draw_undo_delete_last_stamp_button(a_display, a_display_list)
    draw_note_buttons(note_shortcut_list, note_entry_box,
                      note_entry_string)
    draw_update_data_files_button()

if __name__ == '__main__': 
    main()
    root.mainloop()
