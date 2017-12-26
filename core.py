# -*- coding: utf-8 -*-

from threading import Thread
from queue import Queue
import numpy as np
import random
import pyaudio
import pygame
import time
import aubio

from shapes import Line, Polygon
from tools import wavelength_to_rgb, pitch_to_note, roundup


class Analyzer:
    def __init__(self, input_n, n_channels=1, samplerate=44100, buffer_size=2048, tolerance=0.8):
        # initialise pyaudio
        p = pyaudio.PyAudio()
        self.q = Queue()

        # open stream
        pyaudio_format = pyaudio.paFloat32
        self.stream = p.open(format=pyaudio_format,
                             channels=n_channels,
                             rate=samplerate,
                             input=True,
                             input_device_index=input_n,
                             frames_per_buffer=buffer_size)

        time.sleep(1)  # needed to properly start the stream

        # setup onset detector
        self.tolerance = tolerance
        win_s = 4096  # fft size
        self.hop_s = buffer_size // 2  # hop size
        self.onset = aubio.onset("default", win_s, self.hop_s, samplerate)
        self.pitch = aubio.pitch("default", win_s, self.hop_s, samplerate)
        self.pitch.set_unit("midi")
        self.pitch.set_tolerance(self.tolerance)
        self.notes = aubio.notes("default", win_s, self.hop_s, samplerate)
        
    def stop(self): 
        self.stream.stop_stream()
        self.stream.close()

    def analyze(self):
        while True:
            # Reads audio buffer, gests pitch main note and presence of a vivid beat
            # Adds analysis in the main queue
            audiobuffer = self.stream.read(self.hop_s, exception_on_overflow=False)
            signal = np.fromstring(audiobuffer, dtype=np.float32)
            pitch = self.pitch(signal)[0]
            new_note = self.notes(signal)
            onset = True if self.onset(signal) else False
            self.q.put((onset, pitch, new_note))


class Visualizer:
    def __init__(self, source, screen=(1248, 768), fullscreen=False):
        self.source = source
        self.screen_size = screen
        self.element_list = []

        # Initialize screen
        pygame.init()
        self.clock = pygame.time.Clock()
        mode = pygame.SRCALPHA if not fullscreen else pygame.SRCALPHA | pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
        self.screen = pygame.display.set_mode(self.screen_size, mode)

        self.current_status = None
        
    def draw(self):
        if not self.source.q.empty():
            # Gets events from the source queue
            b = self.source.q.get()

            # Tick
            if b[0]:
                bg = Polygon(self.screen_size)
                self.element_list.append(bg)
            
            # Note change
            if self.current_status != roundup(b[1]):
                self.current_status = roundup(b[1])
                self.element_list.append(Line(self.screen_size))
                

        self.screen.fill(black)
        for place, el in enumerate(self.element_list):
            if el.size < 1 or el.transparency < 0:
                self.element_list.pop(place)
            else:
                el.draw(self.screen)
            el.animate()
        
        pygame.display.flip()
        self.clock.tick(90)

    def run(self):
        # Start buffer aquisition
        self.t = Thread(target=self.source.analyze, args=())
        self.t.daemon = True
        self.t.start()

        # Start visualiztion
        running = True
        while running:
            # Check if we need to quit
            key = pygame.key.get_pressed()
            if key[pygame.K_q]:
                running = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Draw things
            self.draw()

        self.source.stop()
        pygame.display.quit()
