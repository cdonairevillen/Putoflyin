from zone import Zone
from link import Link


class Graph():

    def __init__(self,
                 zones: dict[str, Zone],
                 connections: list[tuple[str, str]]
                 ) -> None:

        self.zones = zones
        self.build_graph(connections)
        self.links = {}

    def build_graph(self, connections: list[tuple[str, str]]
                    ) -> None:

        for a, b, capacity in connections:
            zone_a = self.zones[a]
            zone_b = self.zones[b]

            link = Link(zone_a, zone_b, capacity)

            if zone_b.zone_type == "blocked":
                continue

            if zone_a.zone_type == "blocked":
                continue

            zone_a.links.append(link)
            zone_a.adjacent.append(zone_b)
            zone_b.links.append(link)
            zone_b.adjacent.append(zone_a)
