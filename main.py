#!/usr/bin/env python
'''
A conway's Game of Life Interactive implementation
Using Numpy for calculation and Tcod for Presentation

Daniel Cortés (Danomax, Researcho)
06 August 2024
'''

import tcod.context
import tcod.event

WIDTH, HEIGHT = 1020, 780  # Window pixel resolution (when not maximized.)
FLAGS = tcod.context.SDL_WINDOW_RESIZABLE | tcod.context.SDL_WINDOW_MAXIMIZED

import os
import sys
import re
import numpy as np
from life_iterate import life_iterate, rule_iterate
from nputils import repeat_n
#from run_length_encoding import decode, encode
from rle import rle_open
def locate_center(buffer,pattern):
    buffer_center = np.divide(buffer.shape,2).astype(int)
    pattern_center = np.divide(pattern.shape,2).astype(int)
    center = np.zeros(2,dtype='uint8')
    center = np.subtract(buffer_center,pattern_center,where=buffer_center>pattern_center)
    return center

def opencell(filename):
    with open(filename) as file:
        list_pattern = []
        for line in file:
            if line[0] != '!':
                list_pattern.append(line.strip())
        pattern = np.zeros(shape=(len(max(list_pattern, key=len)), len(list_pattern)), dtype=np.int8, order='F')
        ind = 0
        for pat in list_pattern:
            pattern[0:len(pat), ind] = np.frombuffer(bytes(pat, 'utf-8'), dtype='uint8') % 2
            ind += 1
        return pattern
def main() -> None:
    """Script entry point."""
    args = sys.argv[1:]
    #CP437 Tileset
    tileset = tcod.tileset.load_tilesheet(os.path.join(os.pardir,'fonts','df repo',
        'LN_EGA8x8.png'), columns=16, rows=16, charmap=tcod.tileset.CHARMAP_CP437
    )
    tcod.tileset.procedural_block_elements(tileset=tileset)
    #tileset = tcod.tileset.load_tilesheet(os.path.join(os.pardir,'fonts',
    #    'arial10x10.png'), columns=16, rows=16, charmap=tcod.tileset.CHARMAP_TCOD
    #)

    with tcod.context.new(  # New window with pixel resolution of width×height.
        width=WIDTH, height=HEIGHT, tileset=tileset, sdl_window_flags=FLAGS
    ) as context:
        console = context.new_console(order="F")  # Console size based on window resolution and tile size.

        buffer = np.zeros((console.width,console.height),dtype = 'uint8',
                          order="F")
        #Carga de archivo con seed (.life) y lo ubica al centro del campo
        location = [0,0]
        filename = ''
        if args:
            if args[0][-3:] == 'rle':
                filename = args[0]
                rlepattern, x,y,rule = rle_open(filename)
                pattern = np.zeros(shape=(len(max(rlepattern,key=len)),len(rlepattern)),dtype=np.int8,order='F')
                ind = 0
                for rle in rlepattern:
                    pattern[0:len(rle),ind] = np.frombuffer(bytes(rle,'utf-8'),dtype='uint8')%2
                    #DeprecationWarning: The binary mode of fromstring is deprecated, as it behaves
                    # surprisingly on unicode inputs. Use frombuffer instead
                    # pattern[0:len(rle),ind] = np.fromstring(rle,dtype='uint8')%2
                    ind+=1

            elif args[0][-5:] == 'cells':
                filename = args[0]
                pattern = opencell(filename)
                #pattern = np.loadtxt(cellfile,dtype='uint8',comments='!')
            else:
                #sure it crash
                pattern = np.loadtxt(args[0],dtype='uint8')
        else:
            filename = os.path.join('all','bunnies11.cells')
            pattern = opencell(filename)
        location = locate_center(buffer, pattern)
        [x,y] = location
        [w,h] = pattern.shape
        #print(str(x)+','+str(y)+','+str(w)+','+str(h))
        buffer[x:x+w,y:y+h] = pattern[0:w,0:h]

        rule = 'B3/S23'
        play = False
        while True:
            console.clear()
            console.print(0, 0, filename, fg=[255, 255, 255])
            console.rgba['bg'][:] = repeat_n(buffer,4)*255
            context.present(console, integer_scaling=True)
            if play:
                buffer = rule_iterate(buffer, rule, 'Moore')
            for event in tcod.event.get():
                context.convert_event(event)  # Sets tile coordinates for mouse events.
                match event:
                    case tcod.event.Quit():
                        raise SystemExit()
                    case tcod.event.KeyDown(sym=tcod.event.KeySym.RETURN):
                        play = not play
                    case tcod.event.WindowResized():
                        if event.type == "WindowSizeChanged":
                            pass  # The next call to context.new_console may return a different size.


if __name__ == "__main__":
    main()
