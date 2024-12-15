import random
from plateau import Plateau, Joueur


class Jeu:
    """Classe principale pour gérer le jeu."""

    def __init__(self, size=50, nb_obstacles=10, nb_etapes=10):
        self.plateau = Plateau(size=size, max_obstacles=nb_obstacles)
        self.nb_etapes = nb_etapes
        self.joueurs = []

    def ajouter_joueur(self, joueur):
        """Ajouter un joueur au jeu."""
        self.joueurs.append(joueur)
        self.plateau.add_joueur(joueur)

    def lancer(self):
        """Lancer le jeu."""
        if all(joueur.position >= self.plateau.size - 1 for joueur in self.plateau.joueurs):
            print("\nTous les joueurs ont terminé la partie.")
            return  # Empêche de relancer la partie

        print("### Début du jeu ###")
        self.plateau.run()
        print("\nTous les joueurs ont terminé la partie.")

    def afficher_resultats(self):
        """Afficher les résultats des joueurs."""
        print("\n### Résultats ###")
        for joueur in self.joueurs:
            print(f"{joueur.avatar._nom} - Points : {joueur.points}")
        gagnant = max(self.joueurs, key=lambda j: j.points)
        print(f"\nLe gagnant est : {gagnant.avatar._nom} avec {gagnant.points} points !")
        print("\nÉtat final du plateau :")
        for case in self.plateau.cases:
            print(case)
