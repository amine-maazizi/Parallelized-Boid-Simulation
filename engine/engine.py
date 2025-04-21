from engine.utils import *

from engine.boids import Boid
from engine.performance import Performance

from mpi4py import MPI
import numpy as np


class Engine:

    def __init__(self, n=500):
        # MPI initialization
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()
        self.size = self.comm.Get_size()
        self.grid_size = int(np.sqrt(self.size))
        assert self.grid_size * self.grid_size == self.size, "ERROR:Number of processes must be a perfect square."

        self.cart_comm = self.comm.Create_cart((self.grid_size, self.grid_size), periods=(True, True), reorder=True) # 2D cartesian topology
        self.coords = self.cart_comm.Get_coords(self.rank) # Get the coordinates of the current process in the grid

        if self.rank == 0:
            print(f"""
            MPI initialized with {self.size} processes in a {self.grid_size}x{self.grid_size} grid.
            Each process will handle a {DIM.x // self.grid_size}x{DIM.y // self.grid_size} subgrid.
            Each process will handle {n // self.size} boids.
            Iniializing the engine with {n} boids...
                  """)
            pg.init()
            self.display = pg.display.set_mode(DIM)
            pg.display.set_caption(TITLE)
            self.clock = pg.time.Clock()
        else:
            self.display = None
            self.clock = None

        # Local subdomain dimensions
        self.local_width = DIM.x // self.grid_size
        self.local_height = DIM.y // self.grid_size
        self.local_x = self.coords[0] * self.local_width
        self.local_y = self.coords[1] * self.local_height
        
        # Initialize boids
        if self.rank == 0:
            self.boids = [Boid(Engine.random_vector(), Engine.random_vector(), 
                              group=1 if random() % 2 else 2) for _ in range(n)]
        else:
            self.boids = []  


        # Prepare boids for each process
        if self.rank == 0:
            boids_per_rank = [[] for _ in range(self.size)]
            for boid in self.boids:
                # Finding the subdomain for each boid
                x_subdomain = int(boid.pos.x // self.local_width)
                y_subdomain = int(boid.pos.y // self.local_height)
                x_subdomain = min(x_subdomain, self.grid_size - 1) # Clamp to avoid index out of range
                y_subdomain = min(y_subdomain, self.grid_size - 1) # Clamp to avoid index out of range

                rank_dest = self.cart_comm.Get_cart_rank((x_subdomain, y_subdomain)) # Get the rank of the process responsible for the subdomain
                boids_per_rank[rank_dest].append(boid)
        else:
            boids_per_rank = None
        
        # Scatter the boids to each process
        self.local_boids = self.comm.scatter(boids_per_rank, root=0)

        # Initialize ghost boids
        self.ghost_boids = []
        
        self.visual_range = 40
        self.protected_range = 8

        self.performance = Performance()

    def process(self):
        for boid in self.boids:
            close_dp, avg_vel, avg_pos, neighbors = v2(0, 0), v2(0, 0), v2(0, 0), 0
            for other in self.boids:
                if boid.pos.distance_to(other.pos) <= self.protected_range:
                    close_dp += (boid.pos - other.pos)
                elif boid.pos.distance_to(other.pos) <= self.visual_range:
                    avg_vel += other.vel
                    avg_pos += other.pos
                    neighbors += 1
            if neighbors > 0:
                avg_vel /= neighbors
                avg_pos /= neighbors
            boid.process(close_dp, avg_vel, avg_pos)


    def render(self):
        for boid in self.boids:
            boid.render(self.display)

        border_surf = pg.Surface(DIM, pg.SRCALPHA) 
        border_surf.fill((0, 0, 0, 0)) 
        pg.draw.rect(border_surf, BOID_COLOR, Rect(MARGIN, DIM - 2 * MARGIN), 2) 
        self.display.blit(border_surf, (0, 0))

    def run(self):
        while True:
            self.performance.start()
            for ev in pg.event.get():
                if ev.type == QUIT or (ev.type == KEYDOWN and ev.key == K_ESCAPE):
                    pg.quit()
                    sys.exit()
            
            self.display.fill(BG_COLOR)

            self.process()
            self.render()

            self.performance.end()
            pg.display.set_caption(f"{TITLE} - FPS: {self.clock.get_fps():.2f} - AVG TIME: {self.performance.average_time() * 1000:.2f} ms - BOIDS: {len(self.boids)}")

            pg.display.update()
            self.clock.tick(FPS)

    @staticmethod
    def random_vector():
        return v2(random() * DIM.x, random() * DIM.y)