# -*- coding: utf-8 -*-

import argparse
import pyaudio

from core import Analyzer, Visualizer

parser = argparse.ArgumentParser()
parser.add_argument("-input", required=False, type=int, help="Audio Input Device")

# Window args
parser.add_argument("-f", action="store_true", help="Run in Fullscreen Mode")
parser.add_argument("-ws", help="Window size")

# Audio pars
parser.add_argument("-c", help="Number of channels", type=int, default=1)
parser.add_argument("-r", help="Sample rate", type=int, default=44100)
parser.add_argument("-b", help="Audio buffer", type=int, default=2048)


args = parser.parse_args()
if not args.input:
    print("No input device specified. Printing list of input devices now: ")
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        print("Device number (%i): %s" % (i, p.get_device_info_by_index(i).get('name')))
    print("Run this program with -input 1, or the number of the input you'd like to use.")
    exit()

screen = args.ws.split('x') if args.ws else  (1248, 748)

source = Analyzer(args.input, n_channels=args.c, samplerate=args.r, buffer_size=args.b)
v = Visualizer(source, screen, args.f)
v.run()