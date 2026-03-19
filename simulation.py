from drone import Drone


class Simulation():

    def __init__(self, paths, nb_drones):

        self.paths = paths
        self.nb_drones = nb_drones
        self.drones = []
        self.turn = 0

    def colored(self, text, color):
        return f"{color.ansi}{text}\033[0m"

    def assign_drones(self):

        for i in range(self.nb_drones):

            best = min(self.paths,
                       key=lambda p: p.total_time())

            best.assign()
            drone = Drone(i + 1, best)
            self.drones.append(drone)

    def finished(self):

        return all(d.finished for d in self.drones)

    def simulate_turn(self):

        self.turn += 1
        print(f"Turn {self.turn}:\n")
        drones_sorted = sorted(self.drones,
                               key=lambda d: d.position,
                               reverse=True)

        moves = []

        for drone in drones_sorted:

            if drone.in_transit:
                moved = drone.try_move()

                if moved:
                    zone = drone.current_zone()
                    moves.append(f"D{drone.id}"
                                 f"-{self.colored(zone.name, zone.color)}")

        for drone in drones_sorted:
            if not drone.in_transit:
                moved = drone.try_move()

                if moved:
                    zone = drone.current_zone()
                    moves.append(f"D{drone.id}"
                                 f"-{self.colored(zone.name, zone.color)}")

        if moves:
            print(" ".join(moves))

    def run(self):
        self.assign_drones()

        while not self.finished():

            self.simulate_turn()
            print()
