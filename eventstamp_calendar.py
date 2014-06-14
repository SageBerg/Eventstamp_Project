'''
eventstamp_calendar.py

Sage Berg
Created March 2014
'''

from tkinter              import *
from eventstamp_class     import Eventstamp
from eventstamp_variables import *
from eventstamp_parser    import *

class Eventstamp_Calendar(object): #needs a clean up
    
    def __init__(self, window_name):
        self.eventstamp_list = make_eventstamp_list() 
        self.date_dict = make_recent_date_dict()
        inverted_date_dict = \
        {date:number for number, date in self.date_dict.items()}
        temp = list()
        for eventstamp in self.eventstamp_list:
            if eventstamp.date in inverted_date_dict:
                temp.append(eventstamp)
        self.eventstamp_list = temp
        self.eventstamp_list.insert(0,\
        Eventstamp\
        (self.date_dict[0][0],self.date_dict[0][1],self.date_dict[0][2], \
        0, 0, 'Other','',3,'','','no stress'))
        self.width = min(99 + len(self.date_dict)*200 + 100, 1599)  
        #width of calendar canvas 

        self.root = Tk()
        self.root.wm_title(window_name)
        self.scrollbar = Scrollbar(self.root, relief=RAISED)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.calendar = Canvas(\
        self.root, width=self.width, height=1440, bg='white', \
        yscrollcommand = self.scrollbar.set)
        self.calendar.pack(side=LEFT, fill=BOTH)
        self.scrollbar.config(command=self.calendar.yview)

        self.draw_blank_calendar()
        self.fill_calendar_with_blocks() #fills calendar with events 
        self.fill_calendar_with_titles() #labels each block in calendar

        self.root.mainloop()

    def draw_blank_calendar(self):
        for hour in range(24): #create the titles and lines for each hour
            self.calendar.create_line(\
            0, hour*60 + 20, self.width, hour*60 + 20) 
            #+20 px to fit titles at top
            hour_title = str(hour%12) + ':00'
            if hour_title == '0:00': #tacky, fix?
                hour_title = '12:00'
            if hour < 12:
                hour_title += ' AM'
            else:
                hour_title += ' PM'
            self.calendar.create_text((50, hour*60 +30), text=hour_title) 
            #place the titles of each hour
            self.calendar.create_text(\
            (self.width -50, hour*60 +30), text=hour_title) 
        self.calendar.create_line(0, 1460, self.width, 1460) 
        #create last line in calendar
        if len(self.date_dict) <  7:
            for i in range(len(self.date_dict)):
                self.calendar.create_text(200 + i*200, 10, \
                text=self.prettyify_date(self.date_dict[i]))
                self.calendar.create_text(200 + i*200, 1470, \
                text=self.prettyify_date(self.date_dict[i]))
        else:
            index = len(self.date_dict) -1
            for i in range(0,7):
                self.calendar.create_text(1400 - i*200, 10, \
                text=self.prettyify_date(self.date_dict[index]))
                self.calendar.create_text(1400 - i*200, 1470, \
                text=self.prettyify_date(self.date_dict[index]))
                index -= 1

    def prettyify_date(self, date_tuple):
        day = str(date_tuple[2])
        month = month_dict[date_tuple[1]]
        year = '20' + str(date_tuple[0])
        prettyified_date = day + ' ' + month + ' ' + year
        return prettyified_date

    def fill_calendar_with_blocks(self):
        inverted_date_dict = \
        {date:number for number, date in self.date_dict.items()}
        for i in range(len(self.eventstamp_list)):
            if self.eventstamp_list[i-1].date in inverted_date_dict and \
               self.eventstamp_list[i].date in inverted_date_dict:
                prev_event = self.eventstamp_list[i-1]
                curr_event = self.eventstamp_list[i]

                block_color = color_dict[curr_event.what.strip()][0] 
                
                topx    = 100 + inverted_date_dict[prev_event.date]*200  
                bottomx = 300 + inverted_date_dict[curr_event.date]*200 
                topy    = 20  + prev_event.hour*60 + prev_event.minute 
                #y is in minutes
                bottomy = 20  + curr_event.hour*60 + curr_event.minute 
                #draws backwards from stamp time
               
                if prev_event.hour == 23 and prev_event.minute == 60:
                    topy = 20
                    topx += 200
                    
                self.calendar.create_rectangle(\
                topx, topy, bottomx, bottomy, fill=block_color, width=0) 
                #width=0 removes default borders around boxes

    def fill_calendar_with_titles(self):
        inverted_date_dict = \
        {date:number for number, date in self.date_dict.items()}
        for i in range(1,len(self.eventstamp_list)):
            duration = self.eventstamp_list[i].minute   + \
                       self.eventstamp_list[i].hour*60  - \
                      (self.eventstamp_list[i-1].minute + \
                       self.eventstamp_list[i-1].hour*60)
            y_change = 0
            if duration < 0:
                duration += 1460
                y_change = -1440
            if self.eventstamp_list[i-1].date in inverted_date_dict and \
               self.eventstamp_list[i].date   in inverted_date_dict and \
               self.eventstamp_list[i].what.strip() != 'Sexual' and \
               duration >= 15:
                
                prev_event = self.eventstamp_list[i-1]
                curr_event = self.eventstamp_list[i]

                text_color = color_dict[curr_event.what.strip()][1]
                
                if self.eventstamp_list[i].note.strip() != '':
                    block_title = curr_event.note.strip()
                else:
                    block_title = curr_event.what.strip() 

                x = 200 + 200*\
                inverted_date_dict[self.eventstamp_list[i].date]
                y = 26  + 60*\
                prev_event.hour + prev_event.minute + y_change

                self.calendar.create_text(
                (x,y), text=block_title, fill=text_color)
        
                if curr_event.who.strip() != '' and duration >= 30: 
                #show people
                    number_of_people = \
                    min(3,len(curr_event.who.strip().split()))
                    people_string = 'with '
                    if number_of_people < 2:
                        separator_list = ['']
                    elif number_of_people == 2:
                        separator_list = [' and ', '']
                    else:
                        separator_list = [', and ', '']
                    if number_of_people > 2:
                        for i in range(number_of_people -2):
                            separator_list.insert(0, ', ')
                    for i in range(number_of_people):
                        people_string += \
                        curr_event.who.strip().split()[i] + \
                        separator_list[i] 
                    self.calendar.create_text(\
                    (x,y + 16), text=people_string, fill=text_color) 

class Happiness_Calendar(Eventstamp_Calendar):

    def fill_calendar_with_blocks(self): 
        inverted_date_dict = \
        {date:number for number, date in self.date_dict.items()}
        for i in range(1,len(self.eventstamp_list)):
            if self.eventstamp_list[i-1].date in inverted_date_dict and \
               self.eventstamp_list[i].date in inverted_date_dict:
                prev_event = self.eventstamp_list[i-1]
                curr_event = self.eventstamp_list[i]

                block_color = \
                happiness_color_dict[curr_event.happiness.strip()][0]
                if curr_event.what == 'Sleep':
                    block_color = 'white' 
                
                topx    = 100 + inverted_date_dict[prev_event.date]*200  
                bottomx = 300 + inverted_date_dict[curr_event.date]*200 
                topy    = 20  + prev_event.hour*60 + prev_event.minute 
                #y is in minutes
                bottomy = 20  + curr_event.hour*60 + curr_event.minute 
                #draws backwards from stamp time
               
                if prev_event.hour == 23 and prev_event.minute == 60:
                    topy = 20
                    topx += 200
                    
                self.calendar.create_rectangle(\
                topx, topy, bottomx, bottomy, fill=block_color, width=0) 

    def fill_calendar_with_titles(self):
        inverted_date_dict = \
        {date:number for number, date in self.date_dict.items()}
        for i in range(1,len(self.eventstamp_list)):
            duration = self.eventstamp_list[i].minute   + \
            self.eventstamp_list[i].hour*60 - \
                      (self.eventstamp_list[i-1].minute + \
                      self.eventstamp_list[i-1].hour*60)
            y_change = 0
            if duration < 0:
                duration += 1460
                y_change = -1440
            if self.eventstamp_list[i-1].date in inverted_date_dict and \
               self.eventstamp_list[i].date in inverted_date_dict and \
               self.eventstamp_list[i].what.strip() != 'Sexual' and \
               duration >= 15:
                
                prev_event = self.eventstamp_list[i-1]
                curr_event = self.eventstamp_list[i]

                text_color = \
                happiness_color_dict[curr_event.happiness.strip()][1]
                
                if self.eventstamp_list[i].note.strip() != '':
                    block_title = curr_event.note.strip()
                else:
                    block_title = curr_event.what.strip() 

                x = 200 + 200*\
                inverted_date_dict[self.eventstamp_list[i].date]
                y = 26  + 60*\
                prev_event.hour + prev_event.minute + y_change

                self.calendar.create_text(\
                (x,y), text=block_title, fill=text_color)
        
                if curr_event.who.strip() != '' and duration >= 30: 
                #show people
                    number_of_people = len(curr_event.who.strip().split())
                    people_string = 'with '
                    if number_of_people < 2:
                        separator_list = ['']
                    elif number_of_people == 2:
                        separator_list = [' and ', '']
                    else:
                        separator_list = [', and ', '']
                    if number_of_people > 2:
                        for i in range(number_of_people -2):
                            separator_list.insert(0, ', ')
                    for i in range(len(curr_event.who.strip().split())):
                        people_string += \
                        curr_event.who.strip().split()[i] + \
                        separator_list[i] 
                    self.calendar.create_text(\
                    (x,y + 16), text=people_string, fill=text_color) 

class People_Calendar(Eventstamp_Calendar):

    def fill_calendar_with_blocks(self): 
        inverted_date_dict = \
        {date:number for number, date in self.date_dict.items()}
        for i in range(1,len(self.eventstamp_list)):
            if self.eventstamp_list[i-1].date in inverted_date_dict and \
               self.eventstamp_list[i].date in inverted_date_dict and \
               self.eventstamp_list[i].who.strip() != '':
                prev_event = self.eventstamp_list[i-1]
                curr_event = self.eventstamp_list[i]

                block_color = color_dict[curr_event.what.strip()][0] 
                
                topx    = 100 + inverted_date_dict[prev_event.date]*200  
                bottomx = 300 + inverted_date_dict[curr_event.date]*200 
                topy    = 20  + prev_event.hour*60 + prev_event.minute 
                #y is in minutes
                bottomy = 20  + curr_event.hour*60 + curr_event.minute 
                #draws backwards from stamp time
               
                if prev_event.hour == 23 and prev_event.minute == 60:
                    topy = 20
                    topx += 200
                    
                self.calendar.create_rectangle(\
                topx, topy, bottomx, bottomy, fill=block_color, width=0) 

    def fill_calendar_with_titles(self):
        inverted_date_dict = \
        {date:number for number, date in self.date_dict.items()}
        for i in range(1,len(self.eventstamp_list)):
            duration = self.eventstamp_list[i].minute   + \
                       self.eventstamp_list[i].hour*60  - \
                      (self.eventstamp_list[i-1].minute + \
                       self.eventstamp_list[i-1].hour*60)
            y_change = 0
            if duration < 0:
                duration += 1460
                y_change = -1440
            if self.eventstamp_list[i].who.strip() != '' and \
               self.eventstamp_list[i-1].date in inverted_date_dict and \
               self.eventstamp_list[i].date in inverted_date_dict and \
               self.eventstamp_list[i].what.strip() != 'Sexual' and \
               duration >= 15:
                
                prev_event = self.eventstamp_list[i-1]
                curr_event = self.eventstamp_list[i]

                text_color = color_dict[curr_event.what.strip()][1]
                
                if self.eventstamp_list[i].note.strip() != '':
                    block_title = curr_event.note.strip()
                else:
                    block_title = curr_event.what.strip() 

                x = 200 + 200*\
                inverted_date_dict[self.eventstamp_list[i].date]
                y = 26  + 60*\
                prev_event.hour + prev_event.minute + y_change

                self.calendar.create_text(\
                (x,y), text=block_title, fill=text_color)

                if curr_event.who.strip() != '' and duration >= 30: 
                #show people
                    number_of_people = len(curr_event.who.strip().split())
                    people_string = 'with '
                    if number_of_people < 2:
                        separator_list = ['']
                    elif number_of_people == 2:
                        separator_list = [' and ', '']
                    else:
                        separator_list = [', and ', '']
                    if number_of_people > 2:
                        for i in range(number_of_people -2):
                            separator_list.insert(0, ', ')
                    for i in range(len(curr_event.who.strip().split())):
                        people_string += \
                        curr_event.who.strip().split()[i] + \
                        separator_list[i] 
                    self.calendar.create_text(\
                    (x,y + 16), text=people_string, fill=text_color) 

class Stress_Calendar(Eventstamp_Calendar):

    def fill_calendar_with_blocks(self): 
        inverted_date_dict = \
        {date:number for number, date in self.date_dict.items()}
        for i in range(1,len(self.eventstamp_list)):
            if self.eventstamp_list[i-1].date in inverted_date_dict and \
               self.eventstamp_list[i].date in inverted_date_dict: 
                prev_event = self.eventstamp_list[i-1]
                curr_event = self.eventstamp_list[i]

                block_color = stress_color_dict[curr_event.stress][0] 
                
                topx    = 100 + inverted_date_dict[prev_event.date]*200  
                bottomx = 300 + inverted_date_dict[curr_event.date]*200 
                topy    = 20  + prev_event.hour*60 + prev_event.minute 
                #y is in minutes
                bottomy = 20  + curr_event.hour*60 + curr_event.minute 
                #draws backwards from stamp time
               
                if prev_event.hour == 23 and prev_event.minute == 60:
                    topy = 20
                    topx += 200
                    
                self.calendar.create_rectangle(\
                topx, topy, bottomx, bottomy, fill=block_color, width=0) 

    def fill_calendar_with_titles(self):
        inverted_date_dict = \
        {date:number for number, date in self.date_dict.items()}
        for i in range(1,len(self.eventstamp_list)):
            duration = self.eventstamp_list[i].minute   + \
                       self.eventstamp_list[i].hour*60  - \
                      (self.eventstamp_list[i-1].minute + \
                       self.eventstamp_list[i-1].hour*60)
            y_change = 0
            if duration < 0:
                duration += 1460
                y_change = -1440
            if self.eventstamp_list[i-1].date in inverted_date_dict and \
               self.eventstamp_list[i].date in inverted_date_dict and \
               self.eventstamp_list[i].what.strip() != 'Sexual' and \
               duration >= 15:
                
                prev_event = self.eventstamp_list[i-1]
                curr_event = self.eventstamp_list[i]

                text_color = stress_color_dict[curr_event.stress][1]
                
                if self.eventstamp_list[i].note.strip() != '':
                    block_title = curr_event.note.strip()
                else:
                    block_title = curr_event.what.strip() 

                x = 200 + 200*\
                inverted_date_dict[self.eventstamp_list[i].date]
                y = 26  + 60*\
                prev_event.hour + prev_event.minute + y_change

                self.calendar.create_text(\
                (x,y), text=block_title, fill=text_color)

                if curr_event.who.strip() != '' and duration >= 30: 
                #show people
                    number_of_people = len(curr_event.who.strip().split())
                    people_string = 'with '
                    if number_of_people < 2:
                        separator_list = ['']
                    elif number_of_people == 2:
                        separator_list = [' and ', '']
                    else:
                        separator_list = [', and ', '']
                    if number_of_people > 2:
                        for i in range(number_of_people -2):
                            separator_list.insert(0, ', ')
                    for i in range(len(curr_event.who.strip().split())):
                        people_string += \
                        curr_event.who.strip().split()[i] + \
                        separator_list[i] 
                    self.calendar.create_text(\
                    (x,y + 16), text=people_string, fill=text_color) 

def eventstamp_calendar():
    Eventstamp_Calendar('Eventstamp Calendar')

def happiness_calendar():
    Happiness_Calendar('Happiness Calendar')

def people_calendar():
    People_Calendar('People Calendar')

def stress_calendar():
    Stress_Calendar('Stress Calendar')
