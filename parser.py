from typing import List
from zone import Zone
from colors import Colors

VALID_ZONE_TYPES = {
            "normal",
            "priority",
            "restricted",
            "blocked"
            }


class Parser():

    def __init__(self, filepath: str) -> None:

        self.filepath = filepath
        self.nb_drones = 0

        self.lines: List[str] = []
        self.zones: dict[str, Zone] = {}
        self.start_zone: Zone | None = None
        self.end_zone: Zone | None = None
        self.connections: list[tuple[str, str]] = []

    def load_file(self) -> None:

        with open(self.filepath, "r") as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                self.lines.append(line)

    def parse_metadata(self, meta: str) -> dict:

        result = {}

        for item in meta.split():
            if "=" not in item:
                raise ValueError(f"Invalid metadata: {item}")

            key, value = item.split("=")
            result[key] = value
        return result

    def apply_metadata(self, zone: Zone, metadata: dict) -> None:

        if "zone" in metadata:
            ztype = metadata['zone']

            if ztype not in VALID_ZONE_TYPES:

                raise ValueError("Invalid zone type", ztype)

            zone.zone_type = ztype

        if "color" in metadata:
            try:

                zone.color = Colors[metadata["color"].upper()]

            except KeyError:

                zone.color = Colors['DEFAULT']
                print(f"Invalid color: {metadata['color']}"
                      " Setted to the DEFAULT color")
        if "max_drones" in metadata:
            zone.max_drones = int(metadata["max_drones"])

    def parse_zone(self, line: str, zone_type: str) -> None:

        content = line.split(":", 1)[1].strip()
        metadata = {}

        if "[" in content:
            main, meta = content.split("[", 1)
            meta = meta.replace("]", "")
            metadata = self.parse_metadata(meta)

        else:
            main = content

        parts = main.split()

        if len(parts) != 3:
            raise ValueError(f"Invalid zone format: {line}")

        name = parts[0].strip()
        x = int(parts[1])
        y = int(parts[2])

        if name in self.zones:
            raise ValueError(f"Duplicated zone:{name}")

        zone = Zone(name, x, y)
        self.apply_metadata(zone, metadata)

        if zone_type == "start":
            zone.is_start = True
            self.start_zone = zone

        if zone_type == "end":
            zone.is_end = True
            self.end_zone = zone

        self.zones[name] = zone

    def parse_connection(self, line: str) -> None:

        content = line.split(":", 1)[1].strip()
        metadata = {}
        if "[" in content:

            main, meta = content.split("[")

            meta = meta.replace("]", "")
            metadata = self.parse_metadata(meta)

        else:
            main = content

        a, b = main.split("-")
        a = a.strip()
        b = b.strip()
        capacity = int(metadata.get("max_link_capacity", 1))

        self.connections.append((a, b, capacity))

    def get_line_type(self, line: str) -> str:

        if line.startswith("nb_drones:"):
            return "drones"
        if line.startswith("start_hub:"):
            return "start"
        if line.startswith("hub:"):
            return "hub"
        if line.startswith("end_hub:"):
            return "end"
        if line.startswith("connection:"):
            return "connection"

        raise ValueError(f"Invalid line format: {line}")

    def parse_drones(self, line: str) -> None:

        try:
            self.nb_drones = int(line.split(":")[1].strip())
            if self.nb_drones <= 0:
                raise ValueError

        except ValueError:
            raise ValueError(f"Invalid number of drones: {line}")

    def parse(self) -> None:

        for line in self.lines:
            line_type = self.get_line_type(line)

            if line_type == "drones":
                self.parse_drones(line)

            elif line_type in ("start", "hub", "end"):
                self.parse_zone(line, line_type)

            elif line_type == "connection":
                self.parse_connection(line)

        if self.start_zone is None:
            raise ValueError("Missing start zone")

        if self.end_zone is None:
            raise ValueError("Missing end zone")
