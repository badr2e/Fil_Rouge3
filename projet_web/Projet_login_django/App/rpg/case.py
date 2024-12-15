from obstacle import Obstacle

class Case:
    """Classe représentant une case du plateau."""
    def __init__(self, gain, obs=None):
        self.gain = gain  # Points associés à la case
        self.perso = None  # Personnage présent sur la case
        self.obs = obs  # Obstacle éventuel sur la case

    def estLibre(self):
        """Vérifie si la case est libre."""
        return self.perso is None and self.obs is None

    def placerPersonnage(self, perso):
        """Place un personnage sur la case si elle est libre."""
        if self.estLibre():
            self.perso = perso
            return True
        return False

    def enleverPersonnage(self):
        """Retire le personnage de la case."""
        self.perso = None

    def placerObstacle(self, obs):
        """Place un obstacle sur la case."""
        if self.obs is None:
            self.obs = obs

    def getPenalite(self):
        """Renvoie la pénalité de la case."""
        return self.obs.penalite if self.obs else 0

    def __str__(self):
        if self.perso:
            return f"Personnage {self.perso.avatar._nom} (gain = {self.gain})"
        elif self.obs:
            return f"Obstacle (pénalité = {self.obs.penalite})"
        return f"Libre (gain = {self.gain})"
