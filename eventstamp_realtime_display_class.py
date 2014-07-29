'''
evenstamp_realtime_display_class.py

Sage Berg
Created 18 June 2014
'''

from eventstamp_gui    import *
from eventstamp_parser import *

class Realtime_Display(object):
    
    def notify(self):
        eventstamp_list = make_today_eventstamp_list()

        draw_realtime_eventstamp_display(
        get_activity_display_color, 18, 2, eventstamp_list)

        draw_realtime_eventstamp_display(
        get_people_display_color, 19, 2, eventstamp_list)

        draw_realtime_eventstamp_display(
        get_happiness_display_color, 20, 2, eventstamp_list)

        draw_today_stats_canvas(eventstamp_list)

        
