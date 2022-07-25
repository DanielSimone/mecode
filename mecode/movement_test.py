# import printing, printing is mother file if use it, where G is initialized

#import math
#import numpy
import time
import os  # because going to tell in this file where to put the file

# define where you're exporting your pgm file.

# --------------------------------------

from mecode import G

cur_filepath = os.path.dirname(os.path.realpath(__file__))
splitted = cur_filepath.split('/')
n = len(splitted)
cur_dir = ''.join((dir + '/') for dir in splitted[:n - 1])
exportFileDir = cur_dir + "movement_test.pgm"
print("Exporting to file " + str(exportFileDir))

g = G(
    print_lines=False,
    outfile=exportFileDir,
)

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------

# movement test
g.feed(25)
g.move(0, 0, -100) # move -100 (down) in Z
g.dwell(5) # wait 5 sec
g.arc(x=10, y=50, radius=30, direction='CCW') # make a small arc
g.dwell(5) # wait 5 sec
g.rect(10, 10) # make a 10 x 10 rectangle in X, Y
g.dwell(5) # wait 5 sec
g.move(-100, 0, 0) # move -100 (left) in X

g.view('matplotlib')
g.teardown()
