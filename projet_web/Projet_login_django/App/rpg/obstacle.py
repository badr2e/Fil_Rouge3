class Obstacle:
    """Classe représentant un obstacle sur le plateau."""
    def __init__(self, penalite):
        self.penalite = penalite

    def getPenalite(self):
        """Renvoie la pénalité de l'obstacle."""
        return self.penalite

    def __str__(self):
        return f"Obstacle (pénalité = {self.penalite})"
