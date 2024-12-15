from stats import Stat

class Classe:
    """Classe représentant un type de classe (Wizard, Warrior, etc.)"""
    def __init__(self, name, stat):
        self._name = name
        self._stat = stat

    def __str__(self):
        return self._name
