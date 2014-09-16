'''
converts the data in eventstamp_data.txt to an sql db

Sage Berg
Created: 26 April 2014
'''

import sqlite3 
import sys
import eventstamp_parser

def main():
    eventstamp_list = eventstamp_parser.make_eventstamp_list()

    connnection = None

    try:
        connection = sqlite3.connect('data/eventstamp.db')
        cursor = connection.cursor()
    except sqlite3.Error:
        sys.exit(1)
        
    cursor.executescript('''
        DROP TABLE IF EXISTS eventstamps;
        CREATE TABLE eventstamps(

        ID INT,

        Year INT,
        Month INT, 
        Day INT, 
        Hour INT, 
        Minute INT,

        Happiness INT, 
        Stress INT,
        Activity TEXT,
        Location TEXT, 
        Note TEXT,
        People TEXT 

        );''')

    for i in range(len(eventstamp_list)):
        cursor.execute('INSERT INTO eventstamps (ID) VALUES (\'' + \
        str(i) + '\');')

    for i in range(len(eventstamp_list)):
        s = 'UPDATE eventstamps SET '   + \
        ' Year = \''      + str(eventstamp_list[i].year)      + '\',' + \
        ' Month = \''     + str(eventstamp_list[i].month)     + '\',' + \
        ' Day = \''       + str(eventstamp_list[i].day)       + '\',' + \
        ' Hour = \''      + str(eventstamp_list[i].hour)      + '\',' + \
        ' Minute = \''    + str(eventstamp_list[i].minute)    + '\',' + \
        ' Happiness = \'' + str(eventstamp_list[i].happiness) + '\',' + \
        ' Stress = \''    + str(eventstamp_list[i].stress)    + '\',' + \
        ' Activity = \''  + str(eventstamp_list[i].what)      + '\',' + \
        ' Location = \''  + str(eventstamp_list[i].where.replace('\'','')) + '\',' + \
        ' Note = \''      + str(eventstamp_list[i].note.replace('\'',''))  + '\',' + \
        ' People = \''    + str(eventstamp_list[i].who)       + '\''  + \
        ' WHERE ID = \''  + str(i)           + '\';'
        #print(s) 
        cursor.execute(s)

    print('finished putting eventstamps into db')    
    connection.commit()
    connection.close()
