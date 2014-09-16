'''
eventstamp_txt_data_following.py

Sage Berg
Created May 2014
'''

import eventstamp_parser
import eventstamp_variables
from datetime             import *
from eventstamp_class     import *
from eventstamp_variables import *

class Following(object):
    def __init__(self):
        self.eventstamp_list = eventstamp_parser.make_eventstamp_list()

    def following(self):
        print('writing following.txt')

        activity_dict = dict()
        
        for i in range(len(event_list)):
            activity_dict[event_list[i][0].title()] = dict()
            for j in range(len(event_list)):
                activity_dict[event_list[i][0].title()]\
                [event_list[j][0].title()] = 0

        for k in range(len(self.eventstamp_list) -1):
            cur = self.eventstamp_list[k].what
            nex = self.eventstamp_list[k+1].what
            activity_dict[cur][nex] += 1

        outfile = open('data/following.txt', 'w')

        column_titles_string = ', '
        for l in range(len(event_list)):
            column_titles_string += event_list[l][0].title() + ', '
        outfile.write(column_titles_string + '\n')

        for m in range(len(event_list)):
            outfile.write(event_list[m][0].title() + ', ')
            for n in range(len(event_list)):
                outfile.write(\
                str(activity_dict[event_list[m][0].title()]\
                [event_list[n][0].title()]) + ', ')
            outfile.write('\n')
        outfile.close()

def main():
    x = Following()
    x.following()
