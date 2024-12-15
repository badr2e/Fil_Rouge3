import random

class Stat:
    """Gestion des statistiques des personnages"""
    def __init__(self, dictArgs):
        self.strength = dictArgs.get('strength', 1)
        self.magic = dictArgs.get('magic', 1)
        self.agility = dictArgs.get('agility', 1)
        self.speed = dictArgs.get('speed', 1)
        self.charisma = dictArgs.get('charisma', 0)
        self.chance = dictArgs.get('chance', 0)
        self.endurance = random.randint(self.strength + self.agility, 2 * (self.strength + self.agility))
        self.life_point = random.randint(self.endurance, 2 * self.endurance)
        self.attack = self.strength + self.magic + self.agility
        self.defense = self.agility + self.speed + self.endurance

    def __str__(self):
        return str(self.__dict__)
    
    def detailed_str(self):
        # Affichage plus détaillé et lisible des stats
        return (f"Force : {self.strength}, Magie : {self.magic}, Agilité : {self.agility}, "
                f"Vitesse : {self.speed}, Charisme : {self.charisma}, Chance : {self.chance}, "
                f"Endurance : {self.endurance}, PV : {self.life_point}, Attaque : {self.attack}, Défense : {self.defense}")