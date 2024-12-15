from avatar import Hero, Mobs
from stats import Stat
from race import Race
from classe import Classe
from item import Equipment, Bag, Item
from quest import Quest
from versus import Versus  
from jeu import Jeu
from plateau import Joueur


def main():
    # Configuration des races
    statElfe = Stat({'strength': 15, 'magic': 10, 'agility': 10, 'speed': 10, 'charisma': 5, 'chance': 5})  
    elfe = Race('Elfe', statElfe)
    
    statOrc = Stat({'strength': 10, 'magic': 0, 'agility': 5, 'speed': 5, 'charisma': 2, 'chance': 3})  
    orc = Race('Orc', statOrc)

    statHuman = Stat({'strength': 10, 'magic': 5, 'agility': 8, 'speed': 7, 'charisma': 6, 'chance': 4})
    human = Race('Human', statHuman)
    
    # Configuration des classes
    statWizard = Stat({'strength': 5, 'magic': 10, 'agility': 5, 'speed': 5, 'charisma': 10, 'chance': 10})
    wizard = Classe('Wizard', statWizard)

    statWarrior = Stat({'strength': 10, 'magic': 0, 'agility': 5, 'speed': 5, 'charisma': 5, 'chance': 5})
    warrior = Classe('Warrior', statWarrior)
    
    # Création des sacs pour chaque héros
    bagHero1 = Bag({"sizeMax": 10, "items": []})
    bagHero2 = Bag({"sizeMax": 10, "items": []})
    
    # Création du héros principal
    hero = Hero({'name': 'Jean', 'race': elfe, 'classe': wizard, 'bag': bagHero1, 'equipment': [], 'element': 'Fire', 'profession': 'Mage'})
    
    # Création des ennemis
    enemy1 = Mobs({'name': 'Orc1', 'race': orc, 'classe': warrior, 'bag': bagHero1, 'equipment': [], 'element': 'Earth', 'type': 'Soldier'})
    enemy2 = Mobs({'name': 'Orc2', 'race': orc, 'classe': warrior, 'bag': bagHero1, 'equipment': [], 'element': 'Earth', 'type': 'Soldier'})
    
    # Création d’un autre héros pour le mode Versus
    hero2 = Hero({'name': 'Pierre', 'race': human, 'classe': warrior, 'bag': bagHero2, 'equipment': [], 'element': 'Earth', 'profession': 'Guerrier'})
    
    """
    # Lancement de la quête
    sword = Equipment({'classList': ['Warrior'], 'place': 'hand', 'name': 'Épée du dragon', 'type': 'sword', 'space': 2}, Stat({'strength': 5, 'magic': 0, 'agility': 5, 'speed': 5, 'charisma': 0, 'chance': 5}))
    
    quest = Quest({'lAvatar': [enemy1, enemy2], 'lvl': 20, 'gift': sword})
    quest.run(hero)

    # Lancement du mode Versus
    if hero._life > 0:  # Vérifie que le héros a survécu à la quête
        versus = Versus({'player1': hero, 'player2': hero2})  # Initialise le mode Versus
        versus.prepare_for_versus(hero, hero2)  # Prépare les joueurs pour le duel
        versus.run()  # Lancement du combat Versus
    else:
        print(f"{hero._nom} n'est pas en état de combattre dans le mode Versus.")

    """
    # Lancement du mode Plateau
    # Initialisation du jeu
    jeu = Jeu(size=50, nb_obstacles=10, nb_etapes=20)

    # Ajout des joueurs
    joueur1 = Joueur(hero)  # Associer Jean au plateau
    joueur2 = Joueur(hero2)  # Associer Pierre au plateau
    jeu.ajouter_joueur(joueur1)
    jeu.ajouter_joueur(joueur2)

    # Lancer le jeu
    jeu.lancer()


if __name__ == "__main__":
    main()
