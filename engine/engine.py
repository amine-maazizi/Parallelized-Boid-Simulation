from engine.utils import *

from engine.boids import Boid


class Engine:

    def __init__(self, n=500):
        pg.init()
        self.display = pg.display.set_mode(DIM)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        
        self.boids = [Boid(Engine.random_vector(), Engine.random_vector(), group=1 if random() % 2 else 2) for _ in range(n)]
        self.visual_range = 40
        self.protected_range = 8


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
            for ev in pg.event.get():
                if ev.type == QUIT or (ev.type == KEYDOWN and ev.key == K_ESCAPE):
                    pg.quit()
                    sys.exit()
            
            self.display.fill(BG_COLOR)

            self.process()
            self.render()

            pg.display.update()
            self.clock.tick(FPS)

    @staticmethod
    def random_vector():
        return v2(random() * DIM.x, random() * DIM.y)