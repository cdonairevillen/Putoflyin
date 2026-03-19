from dataclasses import dataclass, field
from colors import Colors


@dataclass
class Zone():
    from link import Link
    name: str
    x: int
    y: int

    zone_type: str = "normal"

    color: Colors | None = None

    max_drones: int = 1
    current_drones: int = 0
    is_start: bool = False
    is_end: bool = False
    links: list["Link"] = field(default_factory=list)
    adjacent: list["Zone"] = field(default_factory=list)

    def __hash__(self):
        return hash(self.name)

    @property
    def zone_cost(self) -> float:
        if self.zone_type == "blocked":
            return float('inf')
        if self.zone_type == "restricted":
            return 2
        if self.zone_type == "priority":
            return 0.9
        else:
            return 1

    @property
    def rgb(self):

        if self.color and self.color.rgb:

            return self.color.rgb

        return (200, 200, 200)

    def is_blocked(self):

        return self.zone_type == "blocked"

    def has_capacity(self):

        if self.is_start or self.is_end:
            return True

        return self.current_drones < self.max_drones

    def enter(self):

        if not self.is_start and not self.is_end:
            self.current_drones += 1

    def leave(self):

        if not self.is_start and not self.is_end:
            self.current_drones -= 1
