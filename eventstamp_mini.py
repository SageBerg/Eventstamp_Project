'''
eventstamp.py 
provides a GUI for keeping track of personal activities, 
social interactions, and levels of happiness

Sage Berg
Created 28 July 2014
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

from mini.eventstamp_gui_mini import *
from mini.eventstamp_realtime_display_mini import *

def main():
    eventstamp_list      = make_eventstamp_list()
    note_shortcut_list   = make_note_shortcut_list(eventstamp_list)
    people_shortcut_list = make_people_shortcut_list(eventstamp_list)

    realtime_display_observer = Realtime_Display_Mini()
    realtime_display_observer.notify()

    draw_scales_time_canvas(0,0)
    draw_scales_label_canvas(0, 1, 'End Time Scales')
    scales_list       = draw_time_scales(1, 1, refresh_scales)
    draw_time_scales_check_box(
    END_SCALES_BOOL, 0, 3, 'Use End Scales', scales_list) 
    draw_scales_button(refresh_scales, scales_list, 
                       'Set End Scales to current time',
                       2, 3)
    draw_scales_button(set_scales_to_last_eventstamp, scales_list,
                       'Set End Scales to end time of last eventstamp',
                       4, 3)

    entry_row = 14
    draw_entry_canvas(entry_row, 0)
    people_entry_box, people_string     = draw_people_entry_box(entry_row, 0)
    note_entry_box,   note_entry_string = draw_note_entry_box(entry_row, 3)
    hap_entry, hap_string               = draw_happiness_entry_box(entry_row, 6)

    draw_people_buttons(people_shortcut_list, 
                        people_entry_box, 
                        people_string)
    draw_activity_buttons(people_entry_box, note_entry_box,  hap_entry,
                          stress_bool,      END_SCALES_BOOL, scales_list,
                          realtime_display_observer)
    draw_happiness_buttons(2, 8, hap_entry, hap_string)

    draw_calendar_buttons(12, 0)
    draw_delete_last_stamp_button(2, 8, realtime_display_observer)
    draw_update_data_files_button(0,8)

if __name__ == '__main__': 
    main()
    root.mainloop()
