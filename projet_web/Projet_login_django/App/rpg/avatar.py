from stats import Stat
from item import Bag, Equipment
import random
import math



class Avatar:
    """Classe générique pour les avatars"""
    id = 0

    def __init__(self, targs):
        self._nom = targs['name']
        self._race = targs['race']
        self._classe = targs['classe']
        self._bag = targs['bag']
        self._equipment = targs['equipment']
        self._element = targs['element']
        self._lvl = 1
        self._stat = Stat({'strength': 1, 'magic': 1, 'agility': 1, 'speed': 1, 'charisma': 0, 'chance': 0})
        Avatar.id += 1
        self._id = Avatar.id
        self.sumStat()
        self._life = self._stat.life_point
        self._statistics = {"fight": 0, "win": 0, "maxDamage": 0}

    def sumStat(self):
        """Sommation des statistiques de la race, de la classe et des équipements dans le sac"""
        # Initialiser les stats de base pour éviter une accumulation incorrecte lors de multiples appels
        for key in self._stat.__dict__.keys():
            self._stat.__dict__[key] = 0

        # Ajouter les statistiques de la race
        for key in self._stat.__dict__.keys():
            self._stat.__dict__[key] += self._race._stat.__dict__.get(key, 0)

        # Ajouter les statistiques de la classe
        for key in self._stat.__dict__.keys():
            self._stat.__dict__[key] += self._classe._stat.__dict__.get(key, 0)

        # Ajouter les statistiques des équipements dans le sac
        for item in self._bag._lItems:
            if isinstance(item, Equipment):  # Vérifier que l'objet est un équipement
                for key in self._stat.__dict__.keys():
                    self._stat.__dict__[key] += item._stat.__dict__.get(key, 0)


    def initiative(self):
        min_val = self._stat.speed
        max_val = self._stat.agility + self._stat.chance + self._stat.speed
        return random.randint(min_val, max_val)

    def damages(self):
        """Calcul des dégâts infligés"""
        critique = random.randint(0, 100)
        max_damage = self._stat.attack
        
        if critique > 85:  # Coup critique (15% de chance)
            print(f"{self._nom} inflige un coup critique !")
            max_damage = random.randint(max_damage, 2 * max_damage)  # Multiplication des dégâts critiques
        else:
            max_damage = random.randint(0, max_damage)  # Dégâts normaux

        print(f"{self._nom} inflige {max_damage} dégâts.")
        return round(max_damage)


    def defense(self, damage):
        """Gérer la défense et appliquer les dégâts"""
        dodge = random.randint(0, self._stat.agility + self._stat.chance + self._stat.speed)
        print(f"{self._nom} tente d'esquiver ou de parer.")
        
        if dodge >= (self._stat.agility + self._stat.chance) * 1.5:  # Esquive complète
            print(f"{self._nom} a esquivé l'attaque.")
            return 0  # Aucun dégât
        elif dodge >= (self._stat.agility + self._stat.chance) // 2:  # Esquive partielle
            print(f"{self._nom} a partiellement esquivé l'attaque.")
            damage = round(damage * 0.85)  # Réduire les dégâts de 15% et arrondir
        
        # Réduire les dégâts en fonction de la défense et arrondir
        reduced_damage = max(1, round(damage - (self._stat.defense * 0.2)))  # Minimum de 1
        print(f"{self._nom} subit {reduced_damage} dégâts.")
        
        # Appliquer les dégâts
        self._life -= reduced_damage
        if self._life <= 0:
            self._life = 0
            print(f"{self._nom} est mort.")
        else:
            print(f"PV restants de {self._nom} : {round(self._life)}")




class Hero(Avatar):
    """Classe des héros (joueurs)"""
    def __init__(self, targs):
        super().__init__(targs)
        self._xp = 0
        self._profession = targs['profession']

    def lvl(self):
        lvl = math.floor(self._xp / 100)  #100 XP nécessaires par niveau
        if lvl < 1:
            lvl = 1
        if lvl > self._lvl:
            print("### Nouveau niveau atteint ! ###")
            self.newLvl()
        self._lvl = lvl  # Met à jour le niveau du héros
        return lvl

    def newLvl(self):
        for stat in self._stat.__dict__:
            self._stat.__dict__[stat] += 5
        self._life = self._stat.life_point
        print("### Amélioration des statistiques ###")

    def __str__(self):
        return f"Héros : {self._nom}, Profession : {self._profession}, Niveau : {self._lvl}, Race : {self._race}, Classe : {self._classe}"

class Mobs(Avatar):
    """Classe pour les ennemis"""
    def __init__(self, targs):
        super().__init__(targs)
        self._type = targs['type']
