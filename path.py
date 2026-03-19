

class Path():

    def __init__(self, zones):

        self.zones = zones
        self.links = {}
        self.inner_zones = [zone for zone in zones
                            if not zone.is_start and not zone.is_end]
        self.length = len(zones)
        self.cost = sum(zone.zone_cost for zone in zones)
        self.capacity = self.compute_capacity()
        self.score = self.compute_score()
        self.assigned = 0

        self.build_links()

    def assign(self):

        self.assigned += 1

        return True

    def get_link(self, a, b):

        return self.links.get((a, b)) or self.links.get((b, a))

    def build_links(self):

        for i in range(len(self.zones) - 1):
            a = self.zones[i]
            b = self.zones[i + 1]

            for link in a.links:
                if (link.zone_a == a and link.zone_b == b) or \
                   (link.zone_a == b and link.zone_b == a):
                    self.links[(a, b)] = link

    def total_time(self):

        return self.length + self.assigned / self.capacity

    def compute_capacity(self):

        zone_caps = [zone.max_drones for zone in self.inner_zones]
        linked_caps = [link.max_drones for link in self.links.values()]

        caps = zone_caps + linked_caps

        if not caps:
            return float("inf")

        return min(caps)

    def compute_score(self):
        if self.capacity == 0:
            return float("inf")

        return self.length / self.capacity

    def __lt__(self, other):

        return self.score < other.score
