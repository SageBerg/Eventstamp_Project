'''
eventstamp_variables.py
contains variables to be imported into programs in my self-tracking project

Sage Berg
Created  07 March 2014
Edited   11 June  2014
'''

#the first color is the activity color and the second is the activity title color
event_list = [  
('school','gold', 'black'),
('shopping','bisque', 'black'),		
('clothing & personal care', 'light goldenrod yellow', 'black'),
('aerobic','PeachPuff3', 'black'),
('urinate','light goldenrod', 'black'),
('games','dark khaki', 'black'),
('social','lightblue', 'black'),

('paid work','forest green', 'white'),		
('chores','DeepSkyBlue2', 'black'),
('packing & unpacking', 'light coral', 'black'),
('anaerobic','sandy brown', 'black'),
('defecate','chocolate', 'black'),           
('visual','pink', 'black'),
('idle','gray75', 'black'),
           
('lay in bed','steel blue', 'white'),
('travel','thistle', 'black'),
('clerical chores', 'MediumPurple1', 'black'),
('sexual','indian red', 'black'),
('shower','dark turquoise', 'black'),
('audio','light cyan', 'black'),
('self-track','gray50', 'white'),

('sleep','midnight blue', 'white'),                
('hobby','light slate blue', 'white'),
('food chores', 'olive drab', 'white'),
('eat','dark sea green', 'black'),
('dental','pale green', 'black'),                
('read','dark olive green', 'white'),
('other','black', 'white')               
] #for TK

inverted_event_map = { 
		'school':0,
		'shopping':1,
                'clothing & personal care':2,
		'aerobic':3,
		'urinate':4,
		'games':5,
		'social':6,
		'paid work':7,
		'chores':8,
                'clerical chores':9,
		'anaerobic':10,
		'defecate':11,
		'visual':12,
		'idle':13,
		'lay in bed':14,
		'travel':15,
		'packing & unpacking':16,
                'sexual':17,
		'shower':18,
		'audio':19,
		'self-track':20,
		'sleep':21,
		'hobby':22,
		'food chores':23,
                'eat':24,
		'dental':25,
		'read':26,
		'other':27,
					}

event_map = { 
		0:'school',
		1:'shopping',
                2:'clothing & personal care',
		3:'aerobic',
		4:'urinate',
		5:'games',
		6:'social',
		7:'paid work',
		8:'chores',
                9:'clerical chores',
		10:'anaerobic',
		11:'defecate',
		12:'visual',
		13:'idle',
		14:'lay in bed',
		15:'travel',
		16:'packing & unpacking',
                17:'sexual',
		18:'shower',
		19:'audio',
		20:'self-track',
		21:'sleep',
		22:'hobby',
		23:'food chores',
                24:'eat',
		25:'dental',
		26:'read',
		27:'other',
					}
		

activity_list = [
('school','#FFD700', 'black'),
('shopping','#FFE4C4', 'black'),
('clothing & personal care', '#FAFAD2', 'black'), #		
('aerobic','#CDAF95', 'black'),
('urinate','#EEDD82', 'black'),
('games','#BDB76B', 'black'),
('social','#ADD8E6', 'black'),

('paid work','#228B22', 'white'),		
('chores','#00B2EE', 'black'),
('packing & unpacking', '#F08080', 'black'), #
('anaerobic','#F4A460', 'black'),
('defecate','#D2691E', 'black'),  #wrong hex           
('visual','#FFC0CB', 'black'),
('idle','#BFBFBF', 'black'),
           
('lay in bed','#4682B4', 'white'),
('travel','#D8BFD8', 'black'),
('clerical chores', '#AB82FF', 'black'), #
('sexual','#CD5C5C', 'black'),
('shower','#00CED1', 'black'),
('audio','#E0FFFF', 'black'),
('self-track','#7F7F7F', 'white'),

('sleep','#191970', 'white'),                
('hobby','#8470FF', 'white'),
('food chores', '#6B8E23', 'white'), #
('eat','#8FBC8F', 'black'),
('dental','#98FB98', 'black'),                
('read','#556B2F', 'white'),
('other','#000000', 'white')               
] #for HTML

happiness_color_dict = { '1': ('firebrick', 'white'), 
                         '2': ('tomato', 'black'),
                         '3': ('khaki', 'black'),
                         '4': ('medium sea green', 'black'),
                         '5': ('sea green', 'white') } #for TK

happiness_heatmap_color_dict = { 2.0: '#222202',
                                 2.1: '#4E2F10',
                                 2.2: '#7A3C1E',
                                 2.3: '#A7492B',
                                 2.4: '#D35639',
                                 2.5: '#FF6347',
                                 2.6: '#FC7D55',
                                 2.7: '#F99763',
                                 2.8: '#F6B270',
                                 2.9: '#F3CC7E',
                                 3.0: '#F0E68C',
                                 3.1: '#CCDC87',
                                 3.2: '#A8D281',
                                 3.3: '#84C77C',
                                 3.4: '#60BD76',
                                 3.5: '#3CB371',
                                 3.6: '#39AB6C',
                                 3.7: '#36A367',
                                 3.8: '#349B61',
                                 3.9: '#31935C',
                                 4.0: '#2E8B57'} #for html

stress_color_dict = { 0: ('white', 'black'),
                      1: ('black', 'white') }

month_dict = {  1:'January',
                2:'February',
                3:'March',
                4:'April',
                5:'May',
                6:'June',
                7:'July',
                8:'August',
                9:'September',
                10:'October',
                11:'November',
                12:'December',    }

color_dict = dict()
for event in event_list:
    color_dict[event[0].title()] = (event[1], event[2]) #tuple with bg color then text color

activity_color_dict = dict()
for activity in activity_list:
    activity_color_dict[activity[0].title()] = (activity[1], activity[2]) #tuple with bg color then text color