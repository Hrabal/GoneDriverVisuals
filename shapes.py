# -*- coding: utf-8 -*-
import os
import pygame
import random
from pygame import gfxdraw

from tools import blit_alpha

white = (255, 255, 255)
black = (0, 0, 0)
colors = [(171, 196, 171), (97, 112, 125), (2, 57, 74), (96, 91, 86), (1, 25, 54)]
ck = (127, 33, 33)


class Circle:
    def __init__(self, x, y, color, size, transparency=100):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.base_size = size
        self.transparency = transparency

    def draw(self, surface):
        surface_circle = pygame.Surface((self.size, self.size))
        surface_circle.fill(ck)
        surface_circle.set_colorkey(ck)
        pygame.draw.circle(surface_circle, self.color, (self.base_size//2, self.base_size//2), self.size//2)
        surface_circle.set_alpha(self.transparency)
        surface.blit(surface_circle, (self.x, self.y))

    def animate(self):
        self.size -= 1
        self.transparency -= 15


class CrazyShape:
    drawer = lambda x: False

    def __init__(self, screen_size):
        screen_size = tuple(d * 1.5 for d in screen_size)
        self.size = 2
        self.transparency = 50
        self.color = random.choice(colors)
        self.positions = [list(map(lambda d: random.randrange(d), screen_size)) for _ in range(random.randint(3, 10))]
        self.screen_size = screen_size

    def draw(self, args):
        surface = pygame.Surface(self.screen_size)
        surface.fill(ck)
        surface.set_colorkey(ck)
        self.drawer(*args)
        surface.set_alpha(self.transparency)
        surface.blit(surface, (0,0))

    def animate(self):
        self.size += random.randint(-1, +1)
        for p in self.positions:
            p[0] += random.randint(-5, +5)
            p[1] += random.randint(-5, +5)
        self.transparency -= 1


class Line(CrazyShape):
    drawer = pygame.draw.lines
    
    def draw(self, screen):
        args = (screen, self.color, False, self.positions, self.size)
        super().draw(args)

    def animate(self):
        self.size += random.randint(-3, +3)
        self.transparency -= 3
        for p in self.positions:
            p[0] += random.randint(-15, +15)
            p[1] += random.randint(-15, +15)


class Polygon(CrazyShape):
    drawer = gfxdraw.filled_polygon
    
    def draw(self, screen):
        self.size = 5
        args = (screen, self.positions, self.color)
        super().draw(args)
