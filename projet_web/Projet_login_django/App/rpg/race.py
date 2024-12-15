from stats import Stat

class Race:
    """Classe représentant une race (Elfe, Humain, etc.)"""
    def __init__(self, name, stat):
        self._name = name
        self._stat = stat

    def __str__(self):
        return self._name
