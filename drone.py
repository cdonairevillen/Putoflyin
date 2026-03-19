

class Drone():

    def __init__(self, id, path):

        self.id = id
        self.path = path
        self.position = 0
        self.finished = False
        self.travel_time = 0
        self.in_transit = False
        self.next_zone = None
        self.current_link = None

    def try_move(self):

        if self.finished:
            return False

        if self.in_transit:

            self.travel_time -= 1

            if self.travel_time == 0:
                self.current_link.leave()
                self.current_link = None
                self.next_zone.enter()
                self.position += 1
                self.in_transit = False

                if self.next_zone.is_end:
                    self.finished = True

                return True

            return False

        next_pos = self.position + 1

        if next_pos >= len(self.path.zones):

            return False

        current = self.path.zones[self.position]
        next_zone = self.path.zones[next_pos]
        link = self.path.get_link(current, next_zone)

        if not link.has_capacity():
            return False

        if not next_zone.has_capacity():
            return False

        current.leave()
        link.enter()
        self.current_link = link
        self.in_transit = True
        self.next_zone = next_zone
        self.travel_time = next_zone.zone_cost

        return True

    def current_zone(self):

        return self.path.zones[self.position]
