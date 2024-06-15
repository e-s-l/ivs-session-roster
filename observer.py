"""V classic object file here."""


class Observer:
    """Blueprint for observer object, which primarily links a name to a colour..."""

    def __init__(self, name, colour):
        self.name = name
        self.colour = colour

    def set_colour(self, colour):
        """Observer colour setter."""
        self.colour = colour

    def get_colour(self):
        """Observer colour getter."""
        return self.colour
