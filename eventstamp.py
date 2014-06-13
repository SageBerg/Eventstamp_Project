'''
eventstamp.py 
provides a GUI for keeping track of personal activities

Sage Berg
Created 04 March 2014
'''

from eventstamp_gui_functions import * 
import eventstamp_stats 
#importing eventstamp_stats updates stats when eventstamp.py runs

def main():
    eventstamp_list       = eventstamp_parser.make_eventstamp_list()
    note_shortcut_list    = make_note_shortcut_list(eventstamp_list)
    display, display_list = draw_realtime_eventstamp_display()
    happiness             = draw_happiness_buttons()
    check_box_list        = draw_people_checkboxes(people_list)
    draw_stress_box(stress_bool)
    note_entry_box, note_entry_string = draw_note_entry_box()
    scales_list           = draw_time_scales()
    draw_time_scales_check_box(scales_bool)
    draw_activity_buttons(event_list, happiness, \
                          note_entry_box, stress_bool, \
                          scales_bool, scales_list, display, display_list) #heart of program
    draw_calendar_buttons()
    draw_delete_last_stamp_button(display, display_list)
    draw_note_buttons(note_shortcut_list, note_entry_box, note_entry_string)
    last_stamp_entry = draw_last_stamp_entry()
    draw_last_stamp_button(last_stamp_entry)

if __name__ == '__main__': 
    main()
    root.mainloop()
