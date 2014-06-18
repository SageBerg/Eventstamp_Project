'''
evenstamp_realtime_display_class.py

Sage Berg
Created 18 June 2014
'''

from eventstamp_gui import *

class Realtime_Display(object):
    
    def notify(self):
        draw_realtime_eventstamp_display(get_activity_display_color, 18, 2)
        draw_realtime_eventstamp_display(get_people_display_color, 19, 2)
        draw_realtime_eventstamp_display(get_happiness_display_color, 20, 2)
