'''
eventstamp_html_blocks.py
draws a visualization of time use blocks which will be opened
in an iframe in a calendar html page

Sage Berg
25 Mar 2014
'''
import eventstamp_parser
import eventstamp_variables
from eventstamp_class import Eventstamp

class HTML_Blocks(object): #needs a clean up
    
    def __init__(self):
        self.eventstamp_list = eventstamp_parser.make_eventstamp_list() 
        self.date_dict = eventstamp_parser.make_date_dict()
        self.inverted_date_dict = {date:number for number, date in self.date_dict.items()}
        temp = list()
        for eventstamp in self.eventstamp_list:
            if eventstamp.date in self.inverted_date_dict:
                temp.append(eventstamp)
        self.eventstamp_list = temp
        self.eventstamp_list.insert(0,\
        Eventstamp(self.date_dict[0][0],self.date_dict[0][1],self.date_dict[0][2], \
        0, 0, 'Other','',3,'','','no stress'))
        self.width = min(99 + len(self.date_dict)*200, 1499)  #width of calendar canvas 
        
        self.html_file = open('data/eventstamp_happy_blocks.html', 'w')
        self.html_file.write('<!DOCTYPE html>\n<html>\n<body>\n')
       
        self.draw_dates()
        self.fill_page_with_blocks() #fills calendar with events 
#        self.fill_page_with_titles() #labels each block in the calendar

        self.html_file.write('</body>\n</html>')

    def prettyify_date(self, date_tuple):
        day = str(date_tuple[2])
        month = eventstamp_variables.month_dict[date_tuple[1]]
        year = '20' + str(date_tuple[0])
        prettyified_date = day + '.' + month + '.' + year
        return prettyified_date

    def draw_dates(self):
        for i in range(len(self.date_dict)):
            text = self.prettyify_date(self.date_dict[i])
            self.html_file.write('<div style="position:absolute;left:' + \
                            str(200*i) + 'px"><p>' + text + '</p></div>\n')

    def fill_page_with_blocks(self):
        for i in range(len(self.eventstamp_list)):
            if self.eventstamp_list[i-1].date in self.inverted_date_dict and \
               self.eventstamp_list[i].date in self.inverted_date_dict:
                prev_event = self.eventstamp_list[i-1]
                curr_event = self.eventstamp_list[i]

                block_color = eventstamp_variables.happiness_color_dict[str(curr_event.happiness)][2]
                if curr_event.what == 'Sleep':
                    block_color = '#ffffff'
                
                topx    = 0   + self.inverted_date_dict[prev_event.date]*200 
                topy    = 40  + prev_event.hour*60 + prev_event.minute #y is in minutes 
                bottomx = 200 + self.inverted_date_dict[curr_event.date]*200 
                bottomy = 40  + curr_event.hour*60 + curr_event.minute #draws backwards from stamp time
               
                if prev_event.hour == 23 and prev_event.minute == 60:
                    topy = 40
                    topx += 200
                    bottomx += 200 
                self.html_file.write('<div style=\"position:absolute;left:' + \
                                     str(topx) + 'px;top:' + str(topy) + \
                                     'px;height:' + str(bottomy - topy) + \
                                     'px;width:200px;' + \
                                     'background-color:' + block_color + '\"></div>\n')

    def fill_page_with_titles(self):
        for i in range(1,len(self.eventstamp_list)):
            duration = self.eventstamp_list[i].minute   + self.eventstamp_list[i].hour*60 - \
                      (self.eventstamp_list[i-1].minute + self.eventstamp_list[i-1].hour*60)
            y_change = 0
            if duration < 0:
                duration += 1460
                y_change = -1440
            if self.eventstamp_list[i-1].date in self.inverted_date_dict and \
               self.eventstamp_list[i].date in self.inverted_date_dict and \
               self.eventstamp_list[i].what.strip() != 'Sexual' and duration >= 15:
                
                prev_event = self.eventstamp_list[i-1]
                curr_event = self.eventstamp_list[i]

                text_color = eventstamp_variables.activity_color_dict[curr_event.what.strip()][1]
                
                if self.eventstamp_list[i].note.strip() != '':
                    block_title = curr_event.note.strip()
                else:
                    block_title = curr_event.what.strip()

                x = 200*self.inverted_date_dict[self.eventstamp_list[i].date]
                y = 40 + 60*prev_event.hour + prev_event.minute + y_change

                self.html_file.write('<div style="position:absolute;left:' + \
                                     str(x) + 'px;top:' + str(y) + 'px">' + \
                                     block_title + '</div>\n')

#HTML_Blocks()
