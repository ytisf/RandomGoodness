#!/usr/bin/env python

import sys

import matplotlib.pyplot as plot


"""
Here' a little google sheet to help you generate the graphics you want to get
the constant you need for the Tupper diagram you want.

USE INCOGNITO/PRIVATE MODE!
IF YOU OPEN THIS WITH YOUR GOOGLE ACCOUNT LOGGED IN, ANY OTHER USER WILL BE
ABLE TO SEE YOUR NAME. I CANNOT DISABLE THIS.
https://docs.google.com/spreadsheets/d/1FnOpX3OYJ8pPQbAaXPATkWYT0URbCS3nAyOyE0BYIc0/
"""


WIDTH = 106
HEIGHT = 17
K_TUPPER = 4858450636189713423582095962494202044581400587983244549483093085061934704708809928450644769865524364849997247024915119110411605739177407856919754326571855442057210445735883681829823754139634338225199452191651284348332905131193199953502413758765239264874613394906870130562295813219481113685339535565290850023875092856892694555974281546386510730049106723058933586052544096664351265349363643957125565695936815184334857605266940161251266951421550539554519153785457525756590740540157929001765967965480064427829131488548259914721248506352686630476300 # Tupper's Constant


def tupper(x,y):
    '''
    Tupper's actual formula given int(x) and int(y) returns a BOOL.
    '''
    return 0.5 < ((y//HEIGHT) // (2**(HEIGHT*x + y%HEIGHT))) % 2


def plot_tupper(N=K_TUPPER, name="default"):
    '''
    Get the starting point as N (long) and plot Tupper's formula based on
    that constant.
    '''
    print("Starting to plot graph.")
    plot.rc('patch', antialiased=False)
    for x in xrange(WIDTH):
        for yy in xrange(HEIGHT):
            y = N + yy
            if tupper(x,y):
                plot.bar(left=x, bottom=yy, height=1, width=1, linewidth=0, color='black')
    print("Plotted %s points." % WIDTH)

    plot.axis('scaled')
    buf = 1
    plot.xlim((-buf,WIDTH+buf))
    plot.ylim((-buf,HEIGHT+buf))
    plot.rc('font', size=10)
    plot.xticks(range(0, WIDTH, 100))
    ticks_size = range(0, HEIGHT+1, 4)
    plot.yticks(ticks_size, ['N']+['N + %d'%i for i in ticks_size][1:])
    plot.savefig('%s.png' % name)
    print("File outputed as '%s.png'." % name)
    plot.clf()  # Super important. Apperantly graph details are not lost...
    return


def _half():
    '''
    Will give you the location for a 50/50 black on white Tupper location.
    This was used for testing.
    '''
    white = HEIGHT * (WIDTH/2)
    black = HEIGHT * (WIDTH/2)
    bits = '0' * black
    bits += '1' * white
    return int(bits, 2)*HEIGHT


def _getK(bin_string):
    '''
    Will get a binary string and return the long (converted) to plot.
    '''
    try:
        return int(bin_string, 2)*HEIGHT
    except:
        return False


if __name__ == '__main__':

    all_black_n = "1" * (HEIGHT * WIDTH)        # In binary string
    all_white_n = "0" * (HEIGHT * WIDTH)        # In binary string
    black_tup = _getK(bin_string=all_black_n)   # To int * 17
    white_tup = _getK(bin_string=all_white_n)   # To int * 17
    half = _half()                              # Half in half

    plot_tupper(N=K_TUPPER, name="_Tupper")     # Create with basic Tupper's Constant
    plot_tupper(N=white_tup, name="_White")     # Create all white
    plot_tupper(N=black_tup, name="_Black")     # Create all black
    plot_tupper(N=half, name="_Half")           # Create half in half
