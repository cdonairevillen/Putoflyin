from dataclasses import dataclass
from typing import Any


@dataclass
class Link():

    zone_a: Any
    zone_b: Any

    max_drones: int = 1
    current_drones: int = 0

    def has_capacity(self):

        return self.current_drones < self.max_drones

    def enter(self):

        self.current_drones += 1

    def leave(self):

        self.current_drones -= 1
