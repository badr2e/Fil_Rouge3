from django.db import models
from django.contrib.auth.models import User
from App.rpg.avatar import Hero as RPGHero
from App.rpg.race import Race
from App.rpg.classe import Classe
from App.rpg.item import Bag
from App.rpg.stats import Stat


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_login = models.TextField(unique=True)
    user_password = models.TextField()
    user_mail = models.TextField(unique=True)
    user_date_new = models.DateTimeField(auto_now_add=True)
    user_date_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_login
    
class Item(models.Model):
    TYPE_CHOICES = [
        ('potion', 'Potion'),
        ('plante', 'Plante'),
        ('arme', 'Arme'),
        ('clé', 'Clé'),
        ('armure', 'Pièce d’armure'),
    ]

    nom = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    quantite = models.IntegerField(default=1)
    
    # Relation avec le modèle User
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='items', null=True)

    def __str__(self):
        return f"{self.nom} ({self.type})"
    


class Hero(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="heroes")
    name = models.CharField(max_length=100)
    race = models.CharField(max_length=50)
    hero_class = models.CharField(max_length=50)
    level = models.IntegerField(default=1)
    xp = models.IntegerField(default=0)

    # Champs pour les stats stockées en base
    strength = models.IntegerField(default=0)
    magic = models.IntegerField(default=0)
    agility = models.IntegerField(default=0)
    speed = models.IntegerField(default=0)
    charisma = models.IntegerField(default=0)
    chance = models.IntegerField(default=0)
    endurance = models.IntegerField(default=0)
    life_point = models.IntegerField(default=0)
    attack = models.IntegerField(default=0)
    defense = models.IntegerField(default=0)

    def to_rpg_hero(self):
        """Convertit un Hero Django en un objet RPGHero."""
        if not self.race or not self.hero_class:
            raise ValueError("La race ou la classe du héros est invalide ou manquante.")

        print(f"Conversion en RPGHero : Race = {self.race}, Classe = {self.hero_class}")

        # Initialisation par défaut
        race_stat = Stat({'strength': 10, 'magic': 5, 'agility': 8, 'speed': 7, 'charisma': 6, 'chance': 4})
        classe_stat = Stat({'strength': 5, 'magic': 10, 'agility': 5, 'speed': 5, 'charisma': 10, 'chance': 10})

        # Ajustement des stats en fonction de la race et de la classe
        if self.race == "Elfe":
            race_stat = Stat({'strength': 15, 'magic': 10, 'agility': 10, 'speed': 10, 'charisma': 5, 'chance': 5})
        elif self.race == "Orc":
            race_stat = Stat({'strength': 10, 'magic': 0, 'agility': 5, 'speed': 5, 'charisma': 2, 'chance': 3})

        if self.hero_class == "Wizard":
            classe_stat = Stat({'strength': 5, 'magic': 15, 'agility': 5, 'speed': 5, 'charisma': 10, 'chance': 10})
        elif self.hero_class == "Warrior":
            classe_stat = Stat({'strength': 10, 'magic': 0, 'agility': 5, 'speed': 5, 'charisma': 5, 'chance': 5})

        # Création des objets Race et Classe
        race = Race(self.race, race_stat)
        hero_class = Classe(self.hero_class, classe_stat)
        bag = Bag({'sizeMax': 10, 'items': []})

        print(f"Race stats : {race_stat.__dict__}, Classe stats : {classe_stat.__dict__}")

        # Retour de l'objet RPGHero
        return RPGHero({
            'name': self.name,
            'race': race,
            'classe': hero_class,
            'bag': bag,
            'equipment': [],
            'level': self.level,
            'xp': self.xp,
        })

    def initialize_stats(self):
        """Initialise les stats du héros en fonction de la race et de la classe."""
        rpg_hero = self.to_rpg_hero()
        stats = rpg_hero._stat.__dict__

        # Synchroniser les stats calculées avec le modèle Django
        self.strength = stats['strength']
        self.magic = stats['magic']
        self.agility = stats['agility']
        self.speed = stats['speed']
        self.charisma = stats['charisma']
        self.chance = stats['chance']
        self.endurance = stats['endurance']
        self.life_point = stats['life_point']
        self.attack = stats['attack']
        self.defense = stats['defense']
        print(f"Stats initialisées pour {self.name}.")

    def level_up(self, xp_gain=100):
        """Monte le héros d'un niveau dans le système RPG et synchronise avec Django."""
        rpg_hero = self.to_rpg_hero()

        # Monter de niveau dans le RPG
        old_level = rpg_hero._lvl
        print(f"Avant montée : Niveau = {old_level}, XP = {rpg_hero._xp}")

        # Ajouter une quantité personnalisée d'XP
        rpg_hero._xp += xp_gain
        print(f"XP ajouté : Nouveau XP = {rpg_hero._xp}")

        new_level = rpg_hero.lvl()  # Calculer le nouveau niveau
        print(f"Après montée : Niveau = {new_level}, Stats = {rpg_hero._stat.__dict__}")

        # Synchroniser le niveau, l'XP et les stats avec Django
        self.level = rpg_hero._lvl
        self.xp = rpg_hero._xp

        # Toujours réinitialiser les stats persistantes
        stats = rpg_hero._stat.__dict__
        self.strength = stats['strength']
        self.magic = stats['magic']
        self.agility = stats['agility']
        self.speed = stats['speed']
        self.charisma = stats['charisma']
        self.chance = stats['chance']
        self.endurance = stats['endurance']
        self.life_point = stats['life_point']
        self.attack = stats['attack']
        self.defense = stats['defense']

        self.save()  # Sauvegarder les modifications dans la base
        if new_level > old_level:
            print(f"Héros monté de niveau : {old_level} -> {new_level}")

    def detailed_stats(self):
        """Retourne une chaîne des stats détaillées depuis la base."""
        return (f"Force : {self.strength}, Magie : {self.magic}, Agilité : {self.agility}, "
                f"Vitesse : {self.speed}, Charisme : {self.charisma}, Chance : {self.chance}, "
                f"Endurance : {self.endurance}, PV : {self.life_point}, Attaque : {self.attack}, Défense : {self.defense}")

    def __str__(self):
        return f"{self.name} (Lvl {self.level}, XP {self.xp})"

    def save(self, *args, **kwargs):
        """Surcharge la méthode save pour initialiser les stats uniquement à la création."""
        if not self.pk:  # Si l'objet est créé pour la première fois
            self.initialize_stats()
        super().save(*args, **kwargs)