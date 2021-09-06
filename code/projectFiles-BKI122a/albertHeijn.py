# enter your names and student numbers below
# name1 (s0123456)
# name2 (s6543210)

import math  # a built-in library containing mathematical operations like square root


class Location:
    """
    A class to represent a location, consisting of 'x' and 'y' coordinates.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def position(self):
        return self.x, self.y


class AlbertHeijn(Location):
    """
    A class to represent an Albert Heijn. A location with an added 'name'.
    """

    def __init__(self, name, x, y):
        super().__init__(x, y)
        self.name = name


class TerminalKamer(Location):
    """
    A class to represent a Terminal Kamer. Just a Location with a different name.
    """
    pass


def distance(xy1, xy2):
    """
    Returns the distance between points 'xy1' and 'xy2'
    """
    return math.sqrt(pow(xy1[0] - xy2[0], 2) + pow(xy1[1] - xy2[1], 2))


def closest_ah_distance(tk, ahs):
    """
    Return the distance to the Albert Heijn in 'ahs' that is closest to 'tk'
    """
    tkpos = tk.position()
    ah_positions = [ah.position() for ah in ahs]
    ah_distances = [distance(tkpos, ahpos) for ahpos in ah_positions]
    closest_distance = min(ah_distances)
    return closest_distance


def main():
    # some Albert Heijns in Nijmegen
    albertheijns = [
        AlbertHeijn('Daalseweg', 85, 77),
        AlbertHeijn('Groenestraat', 68, 69),
        AlbertHeijn('van Schevichavenstraat', 79, 83),
        AlbertHeijn('St. Jacobslaan', 70, 58),
        AlbertHeijn('Stationsplein', 70, 82)
    ]
    the_tk = TerminalKamer(75, 56)

    # print the closest distance to an Albert Heijn from the TK
    print(closest_ah_distance(the_tk, albertheijns))


if __name__ == '__main__':
    main()
