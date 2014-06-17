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
    eventstamp_list           = eventstamp_parser.make_eventstamp_list()
    note_shortcut_list        = make_note_shortcut_list(eventstamp_list)
    a_display, a_display_list = draw_realtime_eventstamp_display(
                                get_activity_display_color, 18, 2)
    p_display, p_display_list = draw_realtime_eventstamp_display(
                                get_people_display_color, 19, 2)
    h_display, h_display_list = draw_realtime_eventstamp_display(
                                get_happiness_display_color, 20, 2)

    #draw_stress_box(stress_bool)
    draw_entry_box_canvas()
    draw_end_time_scales_canvas()
    draw_end_time_scale_label_canvas()

    note_entry_box,   note_entry_string = draw_note_entry_box()
    people_entry_box, people_string     = draw_people_entry_box()
    hap_entry, hap_string               = draw_happiness_entry_box()

    scales_list           = draw_time_scales()
    draw_time_scales_check_box(scales_bool)
    draw_scales_button(refresh_scales, scales_list, 
                       'Set End Scales to current time',
                       11, 14)
    draw_scales_button(set_scales_to_last_eventstamp, scales_list,
                       'Set End Scales to end time of last eventstamp',
                       13, 14)

    draw_happiness_buttons(hap_entry, hap_string)
    draw_people_buttons(people_list, people_entry_box, people_string)
    draw_activity_buttons(event_list, hap_entry, 
                          note_entry_box, stress_bool, 
                          scales_bool, scales_list, a_display, 
                          a_display_list, people_entry_box) 

    draw_calendar_buttons()
    draw_delete_last_stamp_button(a_display, a_display_list)
    draw_undo_delete_last_stamp_button(a_display, a_display_list)
    draw_note_buttons(note_shortcut_list, note_entry_box,
                      note_entry_string)
    draw_update_data_files_button()
    #last_stamp_entry = draw_last_stamp_entry()
    #draw_last_stamp_button(last_stamp_entry)

if __name__ == '__main__': 
    main()
    root.mainloop()
