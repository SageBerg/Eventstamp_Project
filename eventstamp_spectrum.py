'''
spectrum.py

Sage Berg
Created 10 April 2014
'''

import sys
import math
import random
import eventstamp_variables

def hexcolor_parse(color):
    '''
    takes string of form '#......' 
    Note: include the # sign in your argument
    returns integers for rr, gg, and bb
    '''
    return int(color[1:3], 16), int(color[3:5], 16), int(color[5:], 16)

def zero_padder(string):
    if len(string) == 1:
        return '0' + string
    if len(string) == 3:
        return string[1:]
    return string

def hexcolor_maker(r, g, b):
    r, g, b = zero_padder(hex(r)[2:]), \
              zero_padder(hex(g)[2:]), \
              zero_padder(hex(b)[2:])
    return '#' + r + g + b

def main(hex_point_alpha, hex_point_beta):
    color_list = list()
    color_list.append('{')

    r1, g1, b1 = hexcolor_parse(hex_point_alpha)
    r2, g2, b2 = hexcolor_parse(hex_point_beta)
    r_dif, g_dif, b_dif = abs(r1 - r2), abs(g1 - g2), abs(b1 - b2)
    
    if r1 == r2:
        r = r1
    if g1 == g2:
        g = g1
    if b1 == b2:
        b = b1
    if r_dif >= g_dif and r_dif >= b_dif:
        for i in range(r_dif): #makes new color each time through the loop
            if r1 < r2:
                r = r1 + i
            elif r1 > r2:
                r = r1 - i
            if g1 < g2:
                g = int(round(g1 + i*(g_dif/r_dif),0)) 
            elif g1 > g2:
                g = int(round(g1 - i*(g_dif/r_dif),0))
            if b1 < b2:
                b = int(round(b1 + i*(b_dif/r_dif),0)) 
            elif b1 > b2:
                b = int(round(b1 - i*(b_dif/r_dif),0))
            color_list.append(str(i/r_dif)) 
            color_list.append(hexcolor_maker(r,g,b))
    elif g_dif >= r_dif and g_dif >= b_dif:
        for i in range(g_dif):
            if g1 < g2:
                g = g1 + i 
            elif g1 > g2:
                g = g1 - i
            if r1 < r2:
                r = int(round(r1 + i*(r_dif/g_dif),0)) 
            elif r1 > r2:
                r = int(round(r1 - i*(r_dif/g_dif),0))
            if b1 < b2:
                b = int(round(b1 + i*(b_dif/g_dif),0)) 
            elif b1 > b2:
                b = int(round(b1 - i*(b_dif/g_dif),0))
            color_list.append(str(i/g_dif)) 
            color_list.append(hexcolor_maker(r,g,b))
    elif b_dif >= r_dif and b_dif >= g_dif:
        for i in range(b_dif):
            if b1 < b2:
                b = b1 + i 
            elif b1 > b2:
                b = b1 - i
            if r1 < r2:
                r = int(round(r1 + i*(r_dif/b_dif),0)) 
            elif r1 > r2:
                r = int(round(r1 - i*(r_dif/b_dif),0))
            if g1 < g2:
                g = int(round(g1 + i*(g_dif/b_dif),0)) 
            elif g1 > g2:
                g = int(round(g1 - i*(g_dif/b_dif),0))
            color_list.append(str(i/b_dif)) 
            color_list.append(hexcolor_maker(r,g,b))
    else:
        color_list.append(hexcolor_maker(r,g,b))
    color_list.append('},\n')

    #f = open('spectrum_' + str(random.randint(100000,999999)) + '.html', 'w')
    #f.write('<!DOCTYPE html>\n<html>\n<body>\n')
    #for i in range(len(color_list)):
    #    f.write('<div style="position:absolute;' \
    #    + 'top:' + str(1*i) + 'px;height:3px;width:1000px;' \
    #    + 'background-color:' + color_list[i] + '"></div>\n')
    #f.write('</body>\n</html>')
    #f.close()

    g = open('eventstamp_spectrum_variables.py', 'a')
    for item in color_list:
        if item[0] == '#':
            g.write('\'' + item + '\',\n')
        elif item[0] == '{' or item[0] == '}':
            g.write(item + '\n')
        else:
            g.write(str(item) + ': ')
    g.close


g = open('eventstamp_spectrum_variables.py', 'w') #to wipe the file clean
g.write('color_dicts_list = [\n')
g.close()

for activity in eventstamp_variables.activity_list:
    main('#FFFFFF', activity[1])

g = open('eventstamp_spectrum_variables.py', 'a')
g.write('\n]')
g.close()
