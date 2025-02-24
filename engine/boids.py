from engine.utils import *


class Boid:

    def __init__(self, position=v2(0, 0), velocity=v2(0, 0), group=1, avoid_factor=0.05, matching_factor=0.05, centering_factor=5e-4, turn_factor=0.5, bias_val=0.001, max_speed=6, min_speed=3):
        self.pos = position
        self.vel = velocity
        self.g = group
        self.af = avoid_factor
        self.mf = matching_factor
        self.cf = centering_factor
        self.tf = turn_factor
        self.bv = bias_val
        self.mas = max_speed
        self.mis = min_speed
    
    def process(self, dp, avg_vel, avg_pos, dt=0.0):
        # Seperation
        self.vel += dp * self.af # Move away from boids in protected range.
        # Alignement
        self.vel += (avg_vel - self.vel) * self.mf # Align with average velocity of boids in visible range.
        # Cohesion
        self.vel += (avg_pos - self.pos) * self.cf # Move toward center of mass of boids in visible range.
        
        # Screen edges (Steer away from edges of display)
        if self.pos.x < MARGIN.x:
            self.vel.x += self.tf
        if self.pos.x > DIM.x - MARGIN.x:
            self.vel.x -= self.tf
        if self.pos.y < MARGIN.y:
            self.vel.y += self.tf
        if self.pos.y > DIM.y - MARGIN.y:
            self.vel.y -= self.tf

        # Bias (This is to model a subset of the group that might know the direction of a food source, or have a preference toward a nest site)
        if self.g == 1: # Bias to the right of the screen
            self.vel.x = (1-self.bv) * self.vel.x + self.bv
        if self.g == 2:
            self.vel.x = (1-self.bv) * self.vel.x - self.bv

        # Speed limits
        speed = self.vel.magnitude()
        if speed > self.mas:
            self.vel *= self.mas / speed
        if speed < self.mis:
            self.vel *= self.mis / speed
        
        self.pos += self.vel


    def render(self, display):
        pg.draw.circle(display, BOID_COLOR, self.pos, 1)