'''
eventstamp.py 
provides a GUI for keeping track of personal activities

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

def main():
    eventstamp_list       = eventstamp_parser.make_eventstamp_list()
    note_shortcut_list    = make_note_shortcut_list(eventstamp_list)
    display, display_list = draw_realtime_eventstamp_display()
    happiness             = draw_happiness_buttons()
    X_draw_happiness_buttons()
    check_box_list        = draw_people_checkboxes(people_list)

    #draw_stress_box(stress_bool)
    draw_entry_box_canvas()
    note_entry_box,   note_entry_string   = draw_note_entry_box()
    people_entry_box, people_entry_string = draw_people_entry_box()
    note_shortcut_box, note_shortcut_string     = \
    draw_add_note_shortcut_entry_box()
    people_shortcut_box, people_shortcut_string = \
    draw_add_people_shortcut_entry_box()
    rm_note_shortcut_box, rm_note_shortcut_string     = \
    draw_remove_note_shortcut_entry_box()
    rm_people_shortcut_box, rm_people_shortcut_string = \
    draw_remove_people_shortcut_entry_box()

    draw_people_buttons(people_list, people_entry_box, people_entry_string)

    scales_list           = draw_time_scales()

    draw_time_scales_check_box(scales_bool)
    draw_activity_buttons(event_list, happiness, \
                          note_entry_box, stress_bool, \
                          scales_bool, scales_list, display, \
                          display_list) #heart of program
    draw_calendar_buttons()
    draw_delete_last_stamp_button(display, display_list)
    draw_note_buttons(note_shortcut_list, note_entry_box, \
                      note_entry_string)
    #last_stamp_entry = draw_last_stamp_entry()
    #draw_last_stamp_button(last_stamp_entry)
    draw_update_data_files_button()

if __name__ == '__main__': 
    main()
    root.mainloop()
