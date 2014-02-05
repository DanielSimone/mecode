""" mecode is a collection of functions desiged to simplify GCode generation.

Relative movements are assumed, unless stated in the function name. Any
function that uses absolute mode always resets back to relative. Similarly, the
arcing plane is always reset to XY after arcing through a different plane.

Author: Jack Minardi
Email: jminardi@seas.harvard.edu

"""

import math
import os

HERE = os.path.dirname(__file__)


class MeCode(object):

    def __init__(self, outfile=None, print_lines=True):
        """
        Parameters
        ----------
        outfile : bool or path
            If a path is specified, the compiled gcode will be writen to that
            file.
        print_lines : bool
            Whether or not to print the compiled GCode to stdout

        """
        if outfile is not None:
            outfile = open(outfile, 'w')
            lines = open(os.path.join(HERE, 'header.txt')).readlines()
            outfile.writelines(lines)
            outfile.write('\n')
        self.outfile = outfile
        self.print_lines = print_lines
        self.setup()

    ### GCode Aliases  ########################################################

    def set_home(self, x=None, y=None, **kwargs):
        args = self._format_args(x, y, kwargs)
        self.write('G92 ' + args)

    def reset_home(self):
        self.write('G92.1')

    def move(self, x=None, y=None, **kwargs):
        args = self._format_args(x, y, kwargs)
        self.write('G1 ' + args)

    def feed(self, rate):
        self.write('F{}'.format(rate))

    def dwell(self, time):
        self.write('G4 P{}'.format(time))

    ### Composed Functions  ###################################################

    def setup(self, outfile=None):
        """ Set the environment into a consistent state to start off.
        """
        self.write('G91')  # start off in relative mode.

    def teardown(self):
        """ Close the outfile file after writing the footer if opened.
        """
        if self.outfile is not None:
            lines = open(os.path.join(HERE, 'footer.txt')).readlines()
            self.outfile.writelines(lines)
            self.outfile.close()

    def home(self):
        self.write('G90')
        self.write('G1 X0 Y0')
        self.write('G91')

    def abs_move(self, x=None, y=None, **kwargs):
        self.write('G90')
        self.move(x=x, y=y, **kwargs)
        self.write('G91')

    def arc(self, direction='CW', radius=1, **kwargs):
        """ Arc to the given point with the given radius and in the given
        direction

        Parameters
        ----------
        points : strs
            Must specify two points as kwargs, e.g. X=5, Y=5
        direction : str (either 'CW' or 'CCW')
            The direction to execute the arc in.
        radius : float
            The radius of the arc.

        """
        dimensions = [k.lower() for k in kwargs.keys()]
        if 'x' in dimensions and 'y' in dimensions:
            plane_selector = 'G17'  # XY plane
        elif 'x' in dimensions:
            plane_selector = 'G18'  # XZ plane
        elif 'y' in dimensions:
            plane_selector = 'G19'  # YZ plane
        else:
            msg = 'Must specify point in 2D as kw arg, e.g. X=10, Y=10'
            raise RuntimeError(msg)

        if direction == 'CW':
            command = 'G2'
        elif direction == 'CCW':
            command = 'G3'

        args = ' '.join([(k.upper() + str(v)) for k, v in kwargs.items()])
        self.write(plane_selector)
        self.write('{} {} R{}'.format(command, args, radius))
        self.write('G17')  # always return back to the default XY plane.

    def rect(self, x, y, direction='CW'):
        """ Trace a rectangle with the given width and height.

        Parameters
        ----------
        x : float
            The width of the rectange in the x dimension.
        y : float
            The heigh of the rectangle in the y dimension.
        direction : either 'CW' or 'CCW'
            Whether to draw the rectangle clockwise or counter clockwise.

        """
        if direction == 'CW':
            self.move(y=y)
            self.move(x=x)
            self.move(y=-y)
            self.move(x=-x)
        else:
            self.move(x=x)
            self.move(y=y)
            self.move(x=-x)
            self.move(y=-y)

    def meander(self, x, y, spacing, orientation='x'):
        """ Infill a rectangle with a square wave meandering pattern. If the
        relevant dimension is not a multiple of the spacing, the spacing will
        be tweaked to ensure the dimensions work out.

        Parameters
        ----------
        x : float
            The width of the rectangle in the x dimension.
        y : float
            The heigh of the rectangle in the y dimension.
        spacing : float
            The space between parallel meander lines.
        orientation : str ('x' or 'y')

        """
        # Major axis is the parallel lines, minor axis is the jog.
        if orientation == 'x':
            major, major_name = x, 'x'
            minor, minor_name = y, 'y'
        else:
            major, major_name = y, 'y'
            minor, minor_name = x, 'x'

        if minor > 0:
            passes = math.ceil(minor / spacing)
        else:
            passes = abs(math.floor(minor / spacing))
        actual_spacing = minor / passes
        if actual_spacing != spacing:
            msg = ';WARNING! meander spacing updated from {} to {}'
            self.write(msg.format(spacing, actual_spacing))
        spacing = actual_spacing
        sign = 1
        for _ in range(int(passes)):
            self.move(**{major_name: (sign * major)})
            self.move(**{minor_name: spacing})
            sign = -1 * sign

    def clip(self, axis='z', direction='+x', height=4):
        """ Move the given axis up to the given height while arcing in the
        given direction.

        Parameters
        ----------
        axis : str
            The axis to move, e.g. 'z'
        direction : str (either +-x or +-y)
            The direction to arc through
        height : float
            The height to end up at

        """
        axis = direction[1]
        orientation = 'CW' if direction[0] == '-' else 'CCW'
        radius = height / 2.0
        kwargs = {
            axis: 0,
            'z': height,
            'direction': orientation,
            'radius': radius,
        }
        self.arc(**kwargs)

    ### AeroTech Specific Functions  ##########################################

    def toggle_pressure(self, com_port):
        self.write('Call togglePress P{}'.format(com_port))

    def set_pressure(self, com_port, value):
        self.write('Call setPress P{} Q{}'.format(com_port, value))

    def set_valve(self, num, value):
        self.write('$DO{}.0={}'.format(num, value))

    ### Private Interface  ####################################################

    def write(self, statement):
        if self.print_lines:
            print statement
        if self.outfile is not None:
            self.outfile.write(statement + '\n')

    def _format_args(self, x, y, kwargs):
        args = []
        if x is not None:
            args.append('X{}'.format(x))
        if y is not None:
            args.append('Y{}'.format(y))
        args += ['{}{}'.format(k, v) for k, v in kwargs.items()]
        args = ' '.join(args)
        return args


if __name__ == '__main__':
    g = MeCode()
    g.meander(10, 10, .5)
    g.teardown()
