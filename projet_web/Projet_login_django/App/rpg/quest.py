import random

class Quest:
    """Gestion des quêtes et des combats"""
    def __init__(self, targs):
        self._lAvatar = targs['lAvatar']  # Liste des ennemis ou adversaires IA
        self._lvl = targs['lvl']          # Niveau de la quête (difficulté)
        self._itemGift = targs['gift']    # Récompense en cas de victoire

    def run(self, hero):
        """Lancement du combat entre le héros et les ennemis IA"""
        round = 1
        print("### Mode Quête ###")
        
        for enemy in self._lAvatar:
            print(f"{hero._nom} affronte {enemy._nom} !")
            while hero._life > 0 and enemy._life > 0:
                print(f"\n--- Round {round} ---")
                print(f"PV de {hero._nom} : {hero._life}")
                print(f"PV de {enemy._nom} : {enemy._life}")
                
                # Initiative : Qui commence ?
                if hero.initiative() > enemy.initiative():
                    print(f"{hero._nom} attaque en premier")
                    enemy.defense(hero.damages())
                    if enemy._life > 0:
                        hero.defense(enemy.damages())
                else:
                    print(f"{enemy._nom} attaque en premier")
                    hero.defense(enemy.damages())
                    if hero._life > 0:
                        enemy.defense(hero.damages())
                
                round += 1

            # Si le héros est mort, arrêter la quête sans récompense
            if hero._life <= 0:
                print(f"{hero._nom} a été vaincu par {enemy._nom}...")
                return  # Terminer la quête sans donner la récompense

            print(f"{hero._nom} a vaincu {enemy._nom} !")

        # Si le héros a survécu à tous les ennemis, lui donner la récompense une fois
        self.reward(hero)


    def reward(self, hero):
        """Récompense le héros en cas de victoire"""
        print(f"Récompense : {self._itemGift}")
        hero._xp += 10 * self._lvl  # Récompense en XP
        print(f"{hero._nom} gagne {10 * self._lvl} points d'expérience et un objet !")
        hero._bag.addItem(self._itemGift)
        hero.lvl()  # Vérifie automatiquement si le héros doit monter de niveau

