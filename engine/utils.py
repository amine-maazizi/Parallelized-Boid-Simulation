import pygame as pg
from pygame.locals import *
import sys
from random import random

v2 = pg.math.Vector2

DIM = v2(1280, 720)
MARGIN = v2(50 * DIM.x / DIM.y, 50)
TITLE = "Boids Simulation"
FPS = 60

BG_COLOR = pg.Color(0, 0, 0)
BOID_COLOR = pg.Color(255, 255, 255)