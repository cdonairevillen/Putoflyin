import colorsys
import sys
import time
from enum import Enum


class Colors(Enum):

    # Formato: ((R, G, B), "Código ANSI")
    DEFAULT = ((200, 200, 200), "\033[0m")
    GREEN = ((80, 200, 120), "\033[32m")
    RED = ((220, 80, 80), "\033[31m")
    BLUE = ((80, 140, 255), "\033[34m")
    YELLOW = ((240, 220, 90), "\033[33m")
    PURPLE = ((180, 120, 255), "\033[35m")
    CRIMSON = ((220, 20, 60), "\033[38;5;197m")
    BLACK = ((0, 0, 0), "\033[30m")
    BROWN = ((165, 42, 42), "\033[33m")
    ORANGE = ((255, 165, 0), "\033[38;5;208m")
    MAROON = ((128, 0, 0), "\033[31m")
    GOLD = ((255, 215, 0), "\033[38;5;220m")
    DARKRED = ((139, 0, 0), "\033[31m")
    VIOLET = ((143, 0, 255), "\033[35m")
    RAINBOW = (None, "DYNAMIC_RAINBOW")

    @property
    def rgb(self):
        return self.value[0]

    @property
    def ansi(self):
        return self.value[1]

    @staticmethod
    def rainbow_rgb(t):

        import colorsys

        hue = (t * 0.002) % 1

        r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)

        return (int(r * 255),
                int(g * 255),
                int(b * 255))

    @staticmethod
    def rainbow_text(text, offset):

        out = ""

        for i, c in enumerate(text):

            hue = (i * 0.08 + offset) % 1

            r, g, b = Colors.rainbow_rgb(hue)

            out += f"\033[38;2;{r};{g};{b}m{c}"

        return out + "\033[0m"

    def get_rainbow_text(text):
        rainbow_str = ""
        n = len(text)
        for i, char in enumerate(text):
            # Generamos un matiz (hue) entre 0.0 y 1.0
            hue = i / n
            # Convertimos HSV a RGB (0-255)
            rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
            r, g, b = [int(x * 255) for x in rgb]

            # Usamos el código ANSI TrueColor (38;2;R;G;B)
            rainbow_str += f"\033[38;2;{r};{g};{b}m{char}"

        return rainbow_str + "\033[0m"

    def animate_rainbow(text):
        offset = 0
        try:
            while True:
                output = ""
                for i, char in enumerate(text):
                    hue = (i / 20 + offset) % 1.0
                    r, g, b = [int(x * 255)
                               for x in colorsys.hsv_to_rgb(hue, 1.0, 1.0)]
                    output += f"\033[38;2;{r};{g};{b}m{char}"

                sys.stdout.write("\r" + output + "\033[0m")
                sys.stdout.flush()
                offset += 0.05
                time.sleep(0.05)
        except KeyboardInterrupt:
            print("\nAnimación detenida.")
