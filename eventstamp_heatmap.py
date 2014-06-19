'''
eventstamp_heatmap.py
writes html file that displays a heatmap representing average ___ by minute

Sage Berg
Created 26 March 2014
'''

import eventstamp_variables as ev
from eventstamp_parser import *
#import eventstamp_heatmap_variables as ehv
from eventstamp_spectrum_variables import color_dicts_list

class HTML_Heatmap(object): 
    
    def __init__(self):
        self.html_file = open('heatmap.html', 'w')

        self.prop_dict = self.make_minute_activity_proportion_dict() 

        self.html_file.write('<!DOCTYPE html>\n<html>\n<body>\n')
        self.draw_heatmap() 
        self.html_file.write('</body>\n</html>')
        self.html_file.close()

    def make_activity_to_freq_dict(self):
        d = dict()
        for i in range(28): #there are 28 activity types
            d[i] = 0
        return d

    def make_minute_activity_proportion_dict(self):
        minute_to_activity_proportion_dict = dict()
        for i in range(0, 1440):
            minute_to_activity_proportion_dict[i] = \
            self.make_activity_to_freq_dict()
        line_list = list()
        f = open('data/time_use_by_minute.txt')
        for line in f:
            if line[0] != 's': #so the titles are not included
                line_list.append(line)
        for i in range(len(line_list)):
            by_minute_values = line_list[i].strip().split(',')
            #print(by_minute_values)
            for j in range(len(by_minute_values)):
                minute_to_activity_proportion_dict[i][j] = \
                by_minute_values[j]
        #print(minute_to_activity_proportion_dict)
        return minute_to_activity_proportion_dict

    def draw_heatmap(self):
        date_dict = make_date_dict()
        x = 0
        for i in range(len(color_dicts_list)):
            for j in range(len(self.prop_dict)):
                color = ''
                prop = int(self.prop_dict[j][i])/len(date_dict)
                for key in color_dicts_list[i].keys():
                    if abs(key - prop) < 0.05:
                        color = color_dicts_list[i][key] 
                        break
                self.html_file.write('<div style="position:absolute;left:' + str(x) + \
                                     'px;top:' + str(j+40) + 'px;height:1px;width:200px;' + \
                                     'background-color:' + color + '"></div>\n')
            x += 200 

#for activity in ev.activity_list:
#    HTML_Heatmap('_' + activity[0].replace(' ','_').replace('-','_').replace('&','_'))

HTML_Heatmap()

    #def draw_school_heatmap(self):
    #    for i in range(0,1440):
    #        for j in range(len(esv.school_colors)):
    #        
    #            color = esv.school_colors[i][1]
    #            self.html_file.write('<div style="position:absolute;left:' + \
    #                             '0px;top:' + str(i+40) + 'px;height:1px;width:200px;' + \
    #                             'background-color:' + color + '"></div>\n')

#class Happiness_Heatmap(object): 
#    
#    def __init__(self):
#        self.minute_to_happiness_dict = self.make_minute_to_happiness_dict()
#        self.html_file = open('happiness_heatmap.html', 'w')
#
#        self.html_file.write('<!DOCTYPE html>\n<html>\n<body>\n')
#        self.draw_heatmap() 
#        self.html_file.write('</body>\n</html>')
#        self.html_file.close()
#
#    def make_minute_to_happiness_dict(self):
#        happiness_by_minute_file = open('data/happiness_by_minute.txt')
#        d = dict()
#        for line in happiness_by_minute_file:
#            key_val_list = line.split(', ')
#            d[key_val_list[0]] = key_val_list[1].strip()
#        return d
#
#    def draw_heatmap(self):
#        for i in range(1,len(self.minute_to_happiness_dict)+1):
#            color = ev.happiness_heatmap_color_dict[round(float(self.minute_to_happiness_dict[str(i)]),1)]
#            self.html_file.write('<div style="position:absolute;left:' + \
#                                 '0px;top:' + str(i+40) + 'px;height:1px;width:200px;' + \
#                                 'background-color:' + color + '"></div>\n')

class People_Heatmap(HTML_Heatmap):
    pass

class Stress_Heatmap(HTML_Heatmap):
    pass

class Activity_Heatmap(HTML_Heatmap):
    pass

#for act in ev.activity_list:
#    subject = act[0].replace(' ','_')
#    subject = subject.replace('-','_')
#    HTML_Heatmap(subject)
#Happiness_Heatmap()
