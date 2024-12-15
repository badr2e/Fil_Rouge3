import random
from avatar import Hero, Mobs
from obstacle import Obstacle  # Importation de la classe Obstacle si utilisée

class Plateau:
    """Classe pour gérer le plateau de jeu."""
    def __init__(self, size=50, max_obstacles=10):
        self.size = size
        self.cases = self.generate_cases(max_obstacles)
        self.joueurs = []  # Liste des joueurs sur le plateau

    def generate_cases(self, max_obstacles):
        """Générer les cases du plateau avec des gains et obstacles."""
        cases = []
        obstacles_places = 0
        for i in range(self.size):
            gain = random.randint(1, 10)
            if i % 5 == 0 and obstacles_places < max_obstacles:
                obs = Obstacle(penalite=gain * 2)  # Obstacle avec pénalité
                cases.append({'gain': gain, 'obs': obs, 'perso': None})
                obstacles_places += 1
            else:
                cases.append({'gain': gain, 'obs': None, 'perso': None})
        return cases


    def add_joueur(self, joueur):
        """Ajouter un joueur sur le plateau."""
        self.joueurs.append(joueur)
        joueur.position = 0  # Placer le joueur sur la première case
        self.cases[0]['perso'] = joueur
        print(f"{joueur.avatar._nom} a été ajouté au plateau.")

    def run(self):
        """Lancer le jeu sur le plateau."""
        print("Début de la partie sur le plateau.")
        joueurs_actifs = [joueur for joueur in self.joueurs if joueur.position < self.size - 1]

        while joueurs_actifs:  # Tant qu'il y a des joueurs actifs
            for joueur in list(joueurs_actifs):  # Créer une copie de la liste pour modification sûre
                if joueur.position >= self.size - 1:
                    print(f"{joueur.avatar._nom} a atteint la dernière case.")
                    joueurs_actifs.remove(joueur)  # Retirer le joueur actif
                    continue

                joueur.deplacer(self.size)
                self.interagir_case(joueur)

                if joueur.position >= self.size - 1:  # Vérifier après le déplacement
                    print(f"{joueur.avatar._nom} a atteint la dernière case.")
                    joueurs_actifs.remove(joueur)
        
        print("\nTous les joueurs ont terminé la partie.")
        self.afficher_resultats()

    def afficher_resultats(self):
        """Afficher un récapitulatif final de la partie."""
        print("\n### Résultats finaux ###")
        for joueur in self.joueurs:
            print(f"{joueur.avatar._nom} - Points : {joueur.points}, Position finale : {joueur.position}")

        gagnants = self.get_gagnants()
        if len(gagnants) == 1:
            print(f"\nLe gagnant est : {gagnants[0].avatar._nom} avec {gagnants[0].points} points !")
        else:
            print("\nIl y a une égalité entre les gagnants :")
            for gagnant in gagnants:
                print(f" - {gagnant.avatar._nom} avec {gagnant.points} points !")

        print("\nÉtat final du plateau :")
        for i, case in enumerate(self.cases):
            if case['perso']:
                print(f"Case {i + 1} : Occupée par {case['perso'].avatar._nom}")
            elif case['obs']:
                print(f"Case {i + 1} : Obstacle (pénalité = {case['obs'].penalite})")
            else:
                print(f"Case {i + 1} : Libre (gain = {case['gain']})")

    def get_gagnants(self):
        """Déterminer le(s) gagnant(s) de la partie."""
        max_points = max(joueur.points for joueur in self.joueurs)
        return [joueur for joueur in self.joueurs if joueur.points == max_points]

    def afficher_plateau(self):
        print("\nÉtat final du plateau :")
        for i, case in enumerate(self.cases):
            perso = case['perso'].avatar._nom if case['perso'] else "Libre"
            obs = case['obs'] if case['obs'] else "Aucun obstacle"
            print(f"Case {i + 1}: Gain = {case['gain']}, {obs}, Personnage = {perso}")

    def interagir_case(self, joueur):
        """Gérer les interactions selon le type de case."""
        if joueur.position <= self.size:  # Vérifier que le joueur est bien sur le plateau
            case = self.cases[joueur.position - 1]
            if case['perso'] is not None and case['perso'] != joueur:
                print(f"{joueur.avatar._nom} tente de se déplacer sur une case occupée. Perd 5 points.")
                joueur.points -= 5
            elif case['obs']:
                penalty = case['obs'].penalite
                print(f"{joueur.avatar._nom} rencontre un obstacle ! Perd {penalty} points.")
                joueur.points -= penalty
            else:
                gain = case['gain']
                print(f"{joueur.avatar._nom} arrive sur une case libre et gagne {gain} points. Total : {joueur.points + gain}.")
                joueur.points += gain
            case['perso'] = joueur  # Met à jour la case avec le joueur actuel
            

class Joueur:
    """Classe pour représenter un joueur sur le plateau."""
    def __init__(self, avatar):
        self.avatar = avatar  # Hero ou Mob
        self.position = 0
        self.points = 0

    def deplacer(self, plateau_size):
        """Déplacer le joueur selon ses caractéristiques."""
        if isinstance(self.avatar, Hero):  # Les héros se déplacent plus loin
            move = random.randint(1, 3)
        elif isinstance(self.avatar, Mobs):  # Les mobs ont une portée limitée
            move = random.randint(1, 2)
        else:
            move = 1

        nouvelle_position = self.position + move
        if nouvelle_position >= plateau_size:
            self.position = plateau_size - 1  # Ne pas dépasser la dernière case
            print(f"{self.avatar._nom} atteint la dernière case.")
        else:
            self.position = nouvelle_position
            print(f"{self.avatar._nom} avance de {move} cases. Nouvelle position : {self.position}")
        return self.position
