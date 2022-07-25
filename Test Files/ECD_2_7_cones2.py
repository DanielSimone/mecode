#import printing, printing is mother file if use it, where G is initialized

import math
import numpy as np
import os # because going to tell in this file where to put the file

#define where you're exporting your pgm file.
#RIGHTNOWTHISONLYWORKSIFITSSQUARE
#--------------------------------------

import mecode
from mecode import G



cur_filepath = os.path.dirname(os.path.realpath(__file__))
splitted = cur_filepath.split('/')
n = len(splitted)
cur_dir = ''.join((dir+'/') for dir in splitted[:n-1])
exportFileDir = cur_dir + "ECD_2_17_SQUARECONES_2layer.pgm"
print("Exporting to file " +  str(exportFileDir))


g = G(
        print_lines = False,
        outfile = exportFileDir,
    )


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
'''

print parameters

'''
COM=5
valve= 'Z'

printZ = 0.125 #in mm
rate = 12.0 #mm/s (rate at which print head moves)
pressure = 55.0 #psi
dw=0 #dwell time
spc=0.125
length = 9
width = 9
sep = 0.5
flip = 1
fly = 2
layers = 2
up = .125

offset = 2

'''
jkljk

'''

def lineY(length,rate,COM,dw):
    g.feed(rate)
    g.toggle_efd_pressure(COM) #pressure ON
    g.dwell(dw)
    g.move(0,length,0)
    g.dwell(dw)
    g.toggle_efd_pressure(COM) #pressure OFF

def displace(sep):
    g.move(sep,0)


'''
meander
'''
def multilayerMeander(layers,pressure,COM,length,width,spc,fly,up):
    for i in range(1,layers):
        g.set_efd_pressure(COM,pressure)
        g.toggle_efd_pressure(COM)
        g.feed(rate)
        g.move(0,0,up)
        g.meander(length, width, spc)
        g.toggle_efd_pressure(COM)
        g.set_efd_pressure(COM,0)
        g.move(0,0,fly)
        g.move(-1*length,-1*width,0)
        g.move(0,0,-1*fly)

    g.set_efd_pressure(COM,pressure)
    g.toggle_efd_pressure(COM)
    g.feed(rate)
    g.move(0,0,up)
    g.meander(length, width, spc)
    g.toggle_efd_pressure(COM)
    g.set_efd_pressure(COM,0)
    g.move(0,0,fly)
    g.move(-1*length,offset,0)
    g.move(0,0,-1*fly)
    g.move(0,0,-1*spc*layers)

#multilayerMeander(layers,pressure,COM,length,width,spc,fly,up)

'''
cone
'''

def cone(layers,pressure,COM,length,width,spc,fly,up):
    for i in range (1,layers+1):
        g.set_efd_pressure(COM,pressure)
        g.feed(rate)
        g.toggle_efd_pressure(COM)
        g.move(0,0,up)
        dir = 1
        tempLength=length
        tempWidth=width
        curLength=length
        curWidth=width
        while tempLength/2 > spc/2 and tempWidth/2 > spc/2:
            if dir == 1:
                x_move = 1
                y_move = 0
            elif dir == 2:
                x_move = 0
                y_move = 1
            elif dir == 3:
                x_move = -1
                y_move = 0
            else:
                x_move = 0
                y_move = -1
                
            g.move(x_move*(tempLength-spc),y_move*(tempWidth-spc))
            
            tempLength = tempLength-abs(x_move)*spc
            tempWidth = tempWidth-abs(y_move)*spc
            curLength = length-tempLength
            curWidth = width-tempWidth
            if dir == 4:
                dir = 1
            else:
                dir=dir+1
        g.toggle_efd_pressure(COM)
        g.move(0,0,fly)
        if dir == 1:
            g.move(-1*(curLength+tempLength-2*spc)/2,-1*(curWidth+tempWidth-2*spc)/2,0)
        elif dir ==2:
            g.move(-1*tempLength)
            g.move(-1*(curLength+tempLength-2*spc)/2,-1*(curWidth+tempWidth-2*spc)/2,0)
        elif dir ==3:
            g.move(-1*tempLength,-1*tempWidth)
            g.move(-1*(curLength+tempLength-6*spc)/2,-1*(curWidth+tempWidth-2*spc)/2,0)
        elif dir ==4:
            g.move(-1*x_move*(tempLength-spc),-1*y_move*(tempWidth))
            g.move(-1*(curLength+tempLength-4*spc)/2,-1*(curWidth+tempWidth-2*spc)/2,0)
        g.move(0,0,-1*fly)

def elegantAbsMove(x_move,y_move,z_move,fly):
    g.move(0,0,fly)
    g.abs_move(x_move,y_move,fly)
    g.abs_move(x_move,y_move,z_move)

elegantAbsMove(40,2,0,fly)    
cone(layers,pressure,COM,length,width,spc,fly,up)

elegantAbsMove(40,17,0,fly)    
cone(layers,pressure,COM,length,width,spc,fly,up)

elegantAbsMove(40,32,0,fly)    
cone(layers,pressure,COM,length,width,spc,fly,up)

g.view('matplotlib')
g.teardown()  
    
    
    
    