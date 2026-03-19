from parser import Parser
from graph import Graph
from dijkstra import Dijkstra
from path import Path
from simulation import Simulation
from visualizer import Visualizer
import pygame


class Fly_in():

    def __init__(self):

        parser = Parser("input.txt")

        parser.load_file()
        parser.parse()

        graph = Graph(parser.zones, parser.connections)
        dijkstra = Dijkstra(graph)
        r_paths = dijkstra.find_paths(parser.start_zone, parser.end_zone)
        paths = [Path(p) for p in r_paths]

        sim = Simulation(paths, parser.nb_drones)
        sim.assign_drones()

        vis = Visualizer(sim, graph)

        running = True

        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if not sim.finished():
                            sim.simulate_turn()

                    if event.key == pygame.K_ESCAPE:
                        running = False

                if sim.finished():
                    running = False

            vis.render()
            vis.clock.tick(60)

        pygame.quit()
