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
exportFileDir = cur_dir + "set_pressure_test.pgm"
print("Exporting to file " + str(exportFileDir))

g = G(
    print_lines=False,
    outfile=exportFileDir,
)

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------

#print parameters
COM = 8

# set pressure test
g.toggle_efd_pressure(COM) # pressure ON
g.set_efd_pressure(COM, 0) # set pressure to 0 psi
g.dwell(5) # wait 5 sec
g.set_efd_pressure(COM, 20) # set pressure to 20 psi
g.dwell(5) # wait 5 sec
g.set_efd_pressure(COM, 40) # set pressure to 40 psi
g.toggle_efd_pressure(COM) # pressure OFF

g.view('matplotlib')
g.teardown()
