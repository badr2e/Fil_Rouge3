class Versus:
    """Classe pour le mode joueur contre joueur (PvP)"""

    def __init__(self, targs):
        """Initialisation du combat PvP"""
        self._player1 = targs['player1']
        self._player2 = targs['player2']

    def run(self):
        """Lancement du combat entre deux joueurs"""
        round = 1
        print("### Mode Versus ###")
        print(f"{self._player1._nom} VS {self._player2._nom}")
        
        while self._player1._life > 0 and self._player2._life > 0:
            print(f"\n--- Round {round} ---")
            print(f"PV de {self._player1._nom} : {self._player1._life}")
            print(f"PV de {self._player2._nom} : {self._player2._life}")

            # Initiative : déterminer l'ordre des actions
            if self._player1.initiative() > self._player2.initiative():
                print(f"{self._player1._nom} attaque en premier")
                self._player2.defense(self._player1.damages())
                if self._player2._life > 0:
                    self._player1.defense(self._player2.damages())
            else:
                print(f"{self._player2._nom} attaque en premier")
                self._player1.defense(self._player2.damages())
                if self._player1._life > 0:
                    self._player2.defense(self._player1.damages())

            round += 1

        # Résultats
        self.display_results()

    def display_results(self):
        """Afficher les résultats du duel"""
        if self._player1._life > 0:
            print(f"{self._player1._nom} remporte le duel avec {self._player1._life} PV restants !")
        elif self._player2._life > 0:
            print(f"{self._player2._nom} remporte le duel avec {self._player2._life} PV restants !")
        else:
            print("Le combat se termine par un KO double.")


    def prepare_for_versus(self, hero, opponent):
            """Prépare les héros pour un combat Versus"""
            print("\n### Préparation pour le Mode Versus ###")
            hero._life = hero._stat.life_point  # Réinitialise les PV du héros
            opponent._life = opponent._stat.life_point  # Réinitialise les PV de l'adversaire
            print(f"{hero._nom} récupère tous ses PV : {hero._life}")
            print(f"{opponent._nom} récupère tous ses PV : {opponent._life}")
