import pygame
from colors import Colors


class Visualizer():

    def __init__(self, simulation, graph):
        pygame.init()

        self.simulation = simulation
        self.graph = graph

        self.width = 1200
        self.height = 800

        xs = [z.x for z in self.graph.zones.values()]
        ys = [z.y for z in self.graph.zones.values()]

        self.min_x = min(xs)
        self.max_x = max(xs)

        self.min_y = min(ys)
        self.max_y = max(ys)

        self.screen = pygame.display.set_mode((self.width, self.height))

        pygame.display.set_caption("Fly-in Drone Simulator")

        self.clock = pygame.time.Clock()

        self.running = True

    def scale(self, x, y):

        graph_w = self.max_x - self.min_x
        graph_h = self.max_y - self.min_y

        scale = min((self.width - 200)/graph_w,
                    (self.height - 200)/graph_h)

        sx = (x - self.min_x) * scale + 100
        sy = (y - self.min_y) * scale + 100
        return sx, sy

    def draw_links(self):

        for zone in self.graph.zones.values():

            x1, y1 = self.scale(zone.x, zone.y)

            for link in zone.links:

                other = (
                    link.zone_b if link.zone_a == zone
                    else link.zone_a)

                x2, y2 = self.scale(other.x, other.y)

                pygame.draw.line(self.screen,
                                 (80, 80, 80),
                                 (x1, y1),
                                 (x2, y2),
                                 2)

    def draw_zones(self):

        size = 20

        for zone in self.graph.zones.values():
            x, y = self.scale(zone.x, zone.y)

            if zone.color == Colors.RAINBOW:
                color = Colors.rainbow_rgb(pygame.time.get_ticks())

            else:
                color = zone.rgb

            pygame.draw.rect(self.screen,
                             color,
                             (x - size//2, y - size//2, size, size))

    def draw_drones(self):
        for drone in self.simulation.drones:
            zone = drone.current_zone()

            x, y = self.scale(zone.x, zone.y)

            pygame.draw.circle(self.screen,
                               (255, 255, 0),
                               (x, y), 6)

    def render(self):

        self.screen.fill((30, 30, 30))
        self.draw_links()
        self.draw_zones()
        self.draw_drones()

        pygame.display.flip()

    def key_input(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return "STEP"

                if event.key == pygame.K_ESCAPE:
                    self.running = False

        return None
