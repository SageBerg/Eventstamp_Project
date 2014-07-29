'''
evenstamp_realtime_display_mini.py

Sage Berg
Created 28 July 2014
'''

from eventstamp_gui_mini import *
from eventstamp_parser   import *

class Realtime_Display_Mini(object):
    
    def notify(self):
        eventstamp_list = make_today_eventstamp_list()

        draw_realtime_eventstamp_display(
        get_activity_display_color, 0, 9, eventstamp_list)

        draw_realtime_eventstamp_display(
        get_people_display_color, 0, 10, eventstamp_list)

        draw_realtime_eventstamp_display(
        get_happiness_display_color, 0, 11, eventstamp_list)
