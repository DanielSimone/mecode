#import printing, printing is mother file if use it, where G is initialized

import math
import numpy as np
import os # because going to tell in this file where to put the file

#define where you're exporting your pgm file.

#--------------------------------------

import mecode
from mecode import G



cur_filepath = os.path.dirname(os.path.realpath(__file__))
splitted = cur_filepath.split('/')
n = len(splitted)
cur_dir = ''.join((dir+'/') for dir in splitted[:n-1])
exportFileDir = cur_dir + "ECD_2_33A_20x5_2layer.pgm"
print ("Exporting to file " +  str(exportFileDir))


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
rate = 12 #mm/s (rate at which print head moves)
pressure = 55 #psi
dw=.01 #dwell time
spc=0.125
length = 20
width = 5
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
    g.toggle_pressure(COM) #pressure ON
    g.dwell(dw)
    g.move(0,length,0)
    g.dwell(dw)
    g.toggle_pressure(COM) #pressure OFF

def displace(sep):
    g.move(sep,0)


'''
meander
'''
def multilayerMeander(layers,pressure,COM,length,width,spc,fly,up):
    for i in range(1,layers):
        g.set_pressure(COM,pressure)
        g.toggle_pressure(COM)
        g.feed(rate)
        g.move(0,0,up)
        g.dwell(dw)
        g.move(2,0,0)
        g.meander(length, width, spc)
        g.toggle_pressure(COM)
        g.set_pressure(COM,0)
        g.move(0,0,fly)
        g.move(-1*length-.5,0,0)
        g.move(0,0,-1*fly-1*spc*(layers-1))
        g.move(0,0,fly+spc*(layers-1))
        g.move(.5,-1*width,0)
        g.move(0,0,-1*fly)

    g.set_pressure(COM,pressure)
    g.toggle_pressure(COM)
    g.feed(rate)
    g.move(0,0,up)
    g.meander(length, width, spc)
    g.move(2,0,0)
    g.toggle_pressure(COM)
    g.set_pressure(COM,0)
    g.move(0,0,fly)
    g.move(-1*length-4,offset,0)
    g.move(0,0,-1*fly)
    g.move(0,0,-1*spc*layers)

def elegantAbsMove(x_move,y_move,z_move,fly):
    g.move(0,0,fly)
    g.abs_move(x_move,y_move,fly)
    g.abs_move(x_move,y_move,z_move)

elegantAbsMove(2,2,0,fly)
multilayerMeander(layers,pressure,COM,length,width,spc,fly,up)

elegantAbsMove(2,9,0,fly)
multilayerMeander(layers,pressure,COM,length,width,spc,fly,up)

elegantAbsMove(2,16,0,fly)
multilayerMeander(layers,pressure,COM,length,width,spc,fly,up)

g.view('matplotlib')
g.teardown()  
    
    
    
    