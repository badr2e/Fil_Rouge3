import random
#from .avatar import Hero, Mobs
from .obstacle import Obstacle  # Importation de la classe Obstacle si utilisée
from .stats import Stat
from .race import Race
from .classe import Classe
from .item import Equipment, Bag, Item
from App.rpg.avatar import Hero, Mobs



class Plateau:
    """Classe pour gérer le plateau de jeu."""
    def __init__(self, size=50, max_monstres=10):
        self.size = size
        self.cases = self.generate_cases(max_monstres)
        self.joueurs = []  # Liste des joueurs sur le plateau

    def generate_cases(self, nb_monstres):
        """Générer les cases du plateau, avec potentiellement des monstres."""
        cases = []
        monstres_places = 0
        for i in range(self.size):
            gain = random.randint(1, 10)  # On peut garder un petit "gain" si vous le souhaitez
            # Structure de stockage : on mettra une liste 'persos' pour tous les avatars sur cette case
            new_case = {'gain': gain, 'persos': []}  
            
            # 20% de chances d'avoir un monstre tant qu'on n'a pas atteint 'nb_monstres'
            if monstres_places < nb_monstres and random.random() < 0.9:
                monster = Mobs({
                    'name': f"Mob_{i}_{monstres_places}",
                    'race': Race("Orc", Stat({'strength':8, 'agility':5, 'speed':5, 'magic':0, 'chance':3})),
                    'classe': Classe("Monster", Stat({'strength':5,'agility':3,'speed':3})),
                    'bag': Bag({'sizeMax': 0, 'items': []}),
                    'equipment': [],
                    'type': 'Mob'
                })
                new_case['persos'].append(monster)
                monstres_places += 1

            cases.append(new_case)
        return cases

    def add_joueur(self, joueur):
        """Ajouter un joueur sur le plateau."""
        self.joueurs.append(joueur)
        joueur.position = 0  # Placer le joueur sur la première case
        self.cases[0]['persos'].append(joueur.avatar)
        print(f"{joueur.avatar.nom} a été ajouté au plateau (case 1).")

    def run(self):
        logs = []
        print("Début de la partie sur le plateau.")
        logs.append("### Début de la partie sur le plateau. ###")
        
        joueurs_actifs = list(self.joueurs)
        while joueurs_actifs:
            for joueur in list(joueurs_actifs):
                if joueur.position >= self.size - 1:
                    logs.append(f"{joueur.avatar.nom} a déjà atteint la dernière case.")
                    joueurs_actifs.remove(joueur)
                    continue

                old_position = joueur.position
                joueur.deplacer(self.size)
                logs.append(f"{joueur.avatar.nom} avance de {joueur.last_move} cases. Nouvelle position : {joueur.position}")

                if joueur.avatar in self.cases[old_position]['persos']:
                    self.cases[old_position]['persos'].remove(joueur.avatar)

                step_logs = self.interagir_case_logs(joueur)  # version qui renvoie logs
                logs.extend(step_logs)

                if joueur.avatar._life <= 0:
                    joueurs_actifs.remove(joueur)
                elif joueur.position >= self.size - 1:
                    logs.append(f"{joueur.avatar.nom} a atteint la dernière case.")
                    joueurs_actifs.remove(joueur)

        logs.append("\nTous les joueurs ont terminé la partie.")
        final_logs = self.afficher_resultats_logs()
        logs.extend(final_logs)
        return logs

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

    def afficher_resultats(self):
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
            if case['persos']:
                occupant_names = [p._nom for p in case['persos']]
                print(f"Case {i + 1} : Occupée par {occupant_names}")
            else:
                print(f"Case {i + 1} : Libre (gain = {case['gain']})")

    def interagir_case(self, joueur):
        position = joueur.position
        if position < 0 or position >= self.size:
            return

        case = self.cases[position]

        # Ajouter le joueur sur la case
        case['persos'].append(joueur.avatar)

        # Lister tous les persos déjà présents sur la case (sans ce joueur) 
        autres = [p for p in case['persos'] if p != joueur.avatar]

        if not autres:
            # Personne d'autre sur la case => (optionnel) gain
            gain = case['gain']
            joueur.points += gain
            print(f"{joueur.avatar.nom} arrive sur une case libre et gagne {gain} points. Total : {joueur.points}.")
            return

        print(f"{joueur.avatar.nom} arrive sur une case OCCUPÉE par {[p.nom for p in autres]}. Combat !")

        # Combattre successivement tous les occupants (monstres ou joueurs)
        for occupant in list(autres):
            if occupant._life <= 0:
                continue  # déjà mort

            # Si occupant est un Mobs ou un Hero, on lance un combat 1v1:
            self.lancer_combat(joueur.avatar, occupant)

            # Vérifier si le joueur est toujours vivant
            if joueur.avatar._life <= 0:
                print(f"{joueur.avatar.nom} est mort au combat.")
                # Retirer le joueur de la case
                if joueur.avatar in case['persos']:
                    case['persos'].remove(joueur.avatar)
                break  # Combat terminé pour ce joueur

            # Sinon, s'il a gagné, l'occupant meurt
            if occupant._life <= 0:
                print(f"{occupant.nom} est mort au combat.")
                case['persos'].remove(occupant)
                # Le joueur pourrait gagner des points/XP ici
                joueur.points += 10
                print(f"{joueur.avatar.nom} gagne 10 points bonus. Total : {joueur.points}.")

    def lancer_combat(self, avatar1, avatar2):
        """Combat 1 vs 1, en 'tour par tour' simplifié."""
        round_count = 1
        while avatar1._life > 0 and avatar2._life > 0:
            print(f"\n--- Round {round_count} ---")
            print(f"{avatar1.nom} PV = {avatar1._life} | {avatar2.nom} PV = {avatar2._life}")

            if avatar1.initiative() >= avatar2.initiative():
                # avatar1 attaque en premier
                dmg = avatar1.damages()
                avatar2.defense(dmg)
                if avatar2._life > 0:
                    dmg2 = avatar2.damages()
                    avatar1.defense(dmg2)
            else:
                # avatar2 attaque en premier
                dmg2 = avatar2.damages()
                avatar1.defense(dmg2)
                if avatar1._life > 0:
                    dmg = avatar1.damages()
                    avatar2.defense(dmg)

            round_count += 1

        # Sortie du combat
        if avatar1._life > 0:
            print(f"{avatar1.nom} a gagné le combat contre {avatar2.nom} !")
        elif avatar2._life > 0:
            print(f"{avatar2.nom} a gagné le combat contre {avatar1.nom} !")
        else:
            print(f"Double KO entre {avatar1.nom} et {avatar2.nom} !")


    def run_one_step(self):
        """Fait un unique tour de jeu, déplace chaque joueur actif, gère les combats.
           Retourne une liste de logs (textes) pour l'UI.
        """
        logs = []
        joueurs_actifs = list(self.joueurs)
        to_remove = []
        
        for joueur in joueurs_actifs:
            if joueur.position >= self.size - 1:
                logs.append(f"{joueur.avatar.nom} est déjà à la dernière case.")
                continue
            if joueur.avatar._life <= 0:
                logs.append(f"{joueur.avatar.nom} est mort. Ne bouge pas.")
                to_remove.append(joueur)
                continue

            old_position = joueur.position
            joueur.deplacer(self.size)
            move_text = f"{joueur.avatar.nom} avance de {joueur.last_move} cases. Position {joueur.position}"
            logs.append(move_text)

            # Retirer l'avatar de l'ancienne case
            if old_position != joueur.position:
                if joueur.avatar in self.cases[old_position]['persos']:
                    self.cases[old_position]['persos'].remove(joueur.avatar)

            # Interaction
            inter_logs = self.interagir_case_one_step(joueur)
            logs.extend(inter_logs)

            # Check si mort après combat
            if joueur.avatar._life <= 0:
                to_remove.append(joueur)
            elif joueur.position >= self.size - 1:
                logs.append(f"{joueur.avatar.nom} atteint la dernière case.")
                to_remove.append(joueur)

        for r in to_remove:
            if r in self.joueurs:
                self.joueurs.remove(r)

        return logs

    def interagir_case_one_step(self, joueur):
        """Idem que 'interagir_case' mais retourne la liste de logs au lieu d'imprimer."""
        logs = []
        position = joueur.position
        if position < 0 or position >= self.size:
            return logs

        case = self.cases[position]
        case['persos'].append(joueur.avatar)

        autres = [p for p in case['persos'] if p != joueur.avatar]
        if not autres:
            gain = case['gain']
            joueur.points += gain
            logs.append(f"{joueur.avatar.nom} arrive sur une case libre et gagne {gain} pts. (Total {joueur.points})")
            return logs

        occupant_names = [p.nom for p in autres]
        logs.append(f"{joueur.avatar.nom} arrive sur une case OCCUPÉE par {occupant_names}. Combat !")

        for occupant in list(autres):
            if occupant._life <= 0:
                continue

            combat_log = self.lancer_combat_one_step(joueur.avatar, occupant)
            logs.extend(combat_log)

            if joueur.avatar._life <= 0:
                logs.append(f"{joueur.avatar.nom} est mort au combat.")
                if joueur.avatar in case['persos']:
                    case['persos'].remove(joueur.avatar)
                break
            if occupant._life <= 0:
                logs.append(f"{occupant.nom} est mort au combat.")
                case['persos'].remove(occupant)
                joueur.points += 10
                logs.append(f"{joueur.avatar.nom} gagne 10 points bonus. Total {joueur.points}.")

        return logs

    def lancer_combat_one_step(self, avatar1, avatar2):
        """Un combat en boucle, on renvoie la liste de logs."""
        logs = []
        round_count = 1
        while avatar1._life > 0 and avatar2._life > 0:
            logs.append(f"\n--- Round {round_count} ---")
            logs.append(f"{avatar1.nom} PV={avatar1._life} | {avatar2.nom} PV={avatar2._life}")

            if avatar1.initiative() >= avatar2.initiative():
                dmg = avatar1.damages()
                logs.append(f"{avatar1.nom} inflige {dmg} dégâts à {avatar2.nom}.")
                avatar2.defense(dmg)
                if avatar2._life > 0:
                    dmg2 = avatar2.damages()
                    logs.append(f"{avatar2.nom} inflige {dmg2} dégâts à {avatar1.nom}.")
                    avatar1.defense(dmg2)
            else:
                dmg2 = avatar2.damages()
                logs.append(f"{avatar2.nom} inflige {dmg2} dégâts à {avatar1.nom}.")
                avatar1.defense(dmg2)
                if avatar1._life > 0:
                    dmg = avatar1.damages()
                    logs.append(f"{avatar1.nom} inflige {dmg} dégâts à {avatar2.nom}.")
                    avatar2.defense(dmg)
            round_count += 1

        if avatar1._life > 0:
            logs.append(f"{avatar1.nom} a gagné le combat contre {avatar2.nom} !")
        elif avatar2._life > 0:
            logs.append(f"{avatar2.nom} a gagné le combat contre {avatar1.nom} !")
        else:
            logs.append(f"Double KO entre {avatar1.nom} et {avatar2.nom} !")

        return logs
    
    def to_dict(self):
        # On convertit chaque case en un dict minimal
        return {
            'size': self.size,
            'cases': [
                {
                    'gain': c['gain'],
                    'persos': [self.avatar_to_dict(p) for p in c['persos']]
                }
                for c in self.cases
            ]
        }

    @staticmethod
    def from_dict(data):
        size = data['size']
        plateau = Plateau(size=size, max_obstacles=0)
        # On reconstruit plateau.cases
        plateau.cases = []
        for c in data['cases']:
            plateau.cases.append({
                'gain': c['gain'],
                'persos': [Plateau.avatar_from_dict(ad) for ad in c['persos']]
            })
        return plateau

    @staticmethod
    def avatar_to_dict(avatar):
        return {
            'name': avatar._nom,
            '_life': avatar._life,
            '_lvl': avatar._lvl,
            # éventuellement plus d’infos...
        }

    @staticmethod
    def avatar_from_dict(ad):
        # Reconstruire un avatar minimal
        from App.rpg.avatar import Hero, Mobs, Avatar
        # vous décidez comment retrouver race/classe ? (Pour la demo, on fait un Hero simple)
        av = Hero({'name': ad['name'], 'race': Race("Elfe", Stat({})), 'classe': Classe("Warrior", Stat({})), 
                   'bag': Bag({'sizeMax':5,'items':[]}), 'equipment':[]})
        av._life = ad['_life']
        av._lvl = ad['_lvl']
        return av
    
    def interagir_case_logs(self, joueur):
        logs = []
        position = joueur.position
        case = self.cases[position]
        case['persos'].append(joueur.avatar)
        
        autres = [p for p in case['persos'] if p != joueur.avatar]
        if not autres:
            gain = case['gain']
            joueur.points += gain
            logs.append(f"{joueur.avatar.nom} arrive sur une case libre et gagne {gain} points. Total : {joueur.points}.")
            return logs
        
        occupant_names = [p.nom for p in autres]
        logs.append(f"{joueur.avatar.nom} arrive sur une case OCCUPÉE par {occupant_names}. Combat !")

        for occupant in list(autres):
            if occupant._life <= 0:
                continue
            combat_logs = self.lancer_combat_logs(joueur.avatar, occupant)
            logs.extend(combat_logs)

            if joueur.avatar._life <= 0:
                logs.append(f"{joueur.avatar.nom} est mort au combat.")
                if joueur.avatar in case['persos']:
                    case['persos'].remove(joueur.avatar)
                break
            if occupant._life <= 0:
                logs.append(f"{occupant.nom} est mort au combat.")
                case['persos'].remove(occupant)
                joueur.points += 10
                logs.append(f"{joueur.avatar.nom} gagne 10 points bonus. Total : {joueur.points}.")
        return logs

    def lancer_combat_logs(self, avatar1, avatar2):
        logs = []
        round_count = 1
        while avatar1._life > 0 and avatar2._life > 0:
            logs.append(f"\n--- Round {round_count} ---")
            logs.append(f"{avatar1.nom} PV={avatar1._life} | {avatar2.nom} PV={avatar2._life}")
            
            if avatar1.initiative() >= avatar2.initiative():
                dmg = avatar1.damages()
                logs.append(f"{avatar1.nom} inflige {dmg} dégâts à {avatar2.nom}.")
                avatar2.defense(dmg)
                if avatar2._life > 0:
                    dmg2 = avatar2.damages()
                    logs.append(f"{avatar2.nom} inflige {dmg2} dégâts à {avatar1.nom}.")
                    avatar1.defense(dmg2)
            else:
                dmg2 = avatar2.damages()
                logs.append(f"{avatar2.nom} inflige {dmg2} dégâts à {avatar1.nom}.")
                avatar1.defense(dmg2)
                if avatar1._life > 0:
                    dmg = avatar1.damages()
                    logs.append(f"{avatar1.nom} inflige {dmg} dégâts à {avatar2.nom}.")
                    avatar2.defense(dmg)
            round_count += 1
        
        if avatar1._life > 0:
            logs.append(f"{avatar1.nom} a gagné le combat contre {avatar2.nom} !")
        elif avatar2._life > 0:
            logs.append(f"{avatar2.nom} a gagné le combat contre {avatar1.nom} !")
        else:
            logs.append(f"Double KO entre {avatar1.nom} et {avatar2.nom} !")
        return logs

    def afficher_resultats_logs(self):
        logs = []
        logs.append("\n### Résultats finaux ###")
        for joueur in self.joueurs:
            logs.append(f"{joueur.avatar.nom} - Points : {joueur.points}, Position finale : {joueur.position}")

        gagnants = self.get_gagnants()
        if len(gagnants) == 1:
            logs.append(f"\nLe gagnant est : {gagnants[0].avatar.nom} avec {gagnants[0].points} points !")
        else:
            logs.append("\nIl y a une égalité entre les gagnants :")
            for gagnant in gagnants:
                logs.append(f" - {gagnant.avatar.nom} avec {gagnant.points} points !")

        logs.append("\nÉtat final du plateau :")
        for i, c in enumerate(self.cases):
            if c['persos']:
                occupant_names = [p.nom for p in c['persos']]
                logs.append(f"Case {i + 1} : Occupée par {occupant_names}")
            else:
                logs.append(f"Case {i + 1} : Libre (gain = {c['gain']})")

        logs.append("\nTous les joueurs ont terminé la partie.")
        return logs


class Joueur:
    def __init__(self, avatar):
        self.avatar = avatar
        self.position = 0
        self.points = 0
        self.last_move = 0  # <-- on initialise last_move à 0

    def deplacer(self, plateau_size):
        if isinstance(self.avatar, Hero):       # Meme Hero que "from App.rpg.avatar import Hero"
            move = random.randint(1, 3)
        elif isinstance(self.avatar, Mobs):
            move = random.randint(1, 2)
        else:
            move = 1

        self.last_move = move
        nouvelle_position = self.position + move
        if nouvelle_position >= plateau_size:
            self.position = plateau_size - 1
            print(f"{self.avatar.nom} atteint la dernière case.")
        else:
            self.position = nouvelle_position
            print(f"{self.avatar.nom} avance de {move} cases. Nouvelle position : {self.position}")
        return self.position
    
    def to_dict(self):
        return {
            'position': self.position,
            'points': self.points,
            'last_move': self.last_move,
            'avatar': Plateau.avatar_to_dict(self.avatar)
        }

    @staticmethod
    def from_dict(data):
        from App.rpg.avatar import Hero, Mobs
        av_data = data['avatar']
        # Reconstruire un avatar minimal
        # si vous avez stocké le type (Hero ou Mobs), on peut faire la distinction
        av = Hero({'name': av_data['name'],'race': Race("Elfe", Stat({})), 'classe': Classe("Warrior", Stat({})),
                   'bag': Bag({'sizeMax':5,'items':[]}), 'equipment':[]})
        av._life = av_data['_life']
        av._lvl = av_data['_lvl']
        j = Joueur(av)
        j.position = data['position']
        j.points = data['points']
        j.last_move = data['last_move']
        return j

