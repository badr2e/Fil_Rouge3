from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .forms import ItemForm, SignUpForm
#from .models import Item, User
from .models import Item as InventoryItem, User
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from .forms import HeroForm
from .models import Hero
from django.contrib.auth.models import AnonymousUser  
from App.rpg.race import Race
from App.rpg.classe import Classe
from App.rpg.item import Equipment, Bag, Item
from App.rpg.quest import Quest
from App.rpg.versus import Versus  
from App.rpg.jeu import Jeu
from App.rpg.plateau import Joueur
from App.rpg.avatar import Mobs
from App.rpg.avatar import Stat
from App.rpg.avatar import Hero as RPGHero


# Vue pour la page de connexion
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Récupère l'utilisateur par son nom d'utilisateur
            user = User.objects.get(user_login=username)
            
            # Utilise check_password pour comparer le mot de passe entré avec le mot de passe haché
            if check_password(password, user.user_password):
                # Si correct, stocke l'ID utilisateur et le login dans la session
                request.session['user_id'] = user.user_id
                request.session['user_login'] = user.user_login
                return redirect('home')
            else:
                # Mot de passe incorrect
                messages.error(request, 'Mot de passe incorrect')
        except User.DoesNotExist:
            # Utilisateur non trouvé
            messages.error(request, 'Utilisateur non trouvé')

    # Affiche la page de connexion pour GET ou en cas d'erreur
    return render(request, 'App/login.html')


# Vue pour la page d'accueil (après connexion)
def home_view(request):  

    # Récupère le login de l'utilisateur à partir de la session
    user_login = request.session.get('user_login')

    # Si l'utilisateur est connecté, affiche la page d'accueil avec son login
    if user_login:
        return render(request, 'App/home.html', {'user_login': user_login})
    else:
        # Si l'utilisateur n'est pas connecté, redirige vers la page de connexion
        return redirect('login')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_password = make_password(form.cleaned_data['user_password'])  # Chiffre le mot de passe
            user.save()
            messages.success(request, "Votre inscription a été réalisée avec succès !")
            return redirect('login')
    else:
        form = SignUpForm()
    
    return render(request, 'App/signup.html', {'form': form})

# Lister tous les objets de l'inventaire
def inventory_list(request):
    user_id = request.session.get('user_id')  # Récupérer l'ID utilisateur depuis la session
    if not user_id:
        # Si l'utilisateur n'est pas connecté, le rediriger vers la page de login
        return redirect('login')
    
    # Récupérer l'utilisateur et ses items
    user = User.objects.get(pk=user_id)
    items = user.items.all()  # Récupérer les items de l'utilisateur
    
    return render(request, 'App/inventory_list.html', {'items': items})


# Vue pour afficher la liste des objets d'inventaire
def inventory_list_view(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    # Filtrer les objets par utilisateur
    items = InventoryItem.objects.filter(user_id=user_id)

    # Rechercher un objet par nom
    search_query = request.GET.get('search', '')
    if search_query:
        items = items.filter(nom__icontains=search_query)

    # Trier par catégorie
    sort_query = request.GET.get('sort', '')
    if sort_query:
        items = items.filter(type=sort_query)

    # Si la requête est AJAX, renvoyer uniquement les lignes du tableau
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        items_html = render_to_string('App/inventory_table.html', {'items': items})
        return JsonResponse({'items_html': items_html})

    # Renvoyer la page complète pour les requêtes non-AJAX
    return render(request, 'App/inventory_list.html', {'items': items})


def add_item(request):
    user_id = request.session.get('user_id')
    print(f"User ID from session: {user_id}")  # Vérifiez l'ID de l'utilisateur

    if not user_id:
        return redirect('login')

    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            new_item = form.save(commit=False)
            try:
                user = User.objects.get(user_id=user_id)
                new_item.user = user
                new_item.save()
                return redirect('inventory_list')
            except User.DoesNotExist:
                print(f"User with ID {user_id} does not exist.")
        else:
            print("Form is not valid.")
    else:
        form = ItemForm()

    return render(request, 'App/add_item.html', {'form': form})


# Mettre à jour la quantité d'un objet
def update_item(request, item_id):
    # Récupérer l'ID de l'utilisateur depuis la session
    user_id = request.session.get('user_id')
    
    if not user_id:
        # Redirige vers la page de connexion si l'utilisateur n'est pas connecté
        return redirect('login')

    # Récupérer l'objet associé à l'utilisateur
    item = get_object_or_404(InventoryItem, id=item_id, user_id=user_id)

    if request.method == 'POST':
        # Passer les données POST au formulaire avec l'instance de l'objet
        form = ItemForm(request.POST, instance=item)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'L\'objet a été mis à jour avec succès.')
            return redirect('inventory_list')
    else:
        # Afficher le formulaire avec l'instance de l'objet
        form = ItemForm(instance=item)

    return render(request, 'App/update_item.html', {'form': form, 'item': item})


# Vue pour supprimer un objet de l'inventaire
def delete_item(request, item_id):
    # Récupérer l'utilisateur connecté depuis la session
    user_id = request.session.get('user_id')
    if not user_id:
        # Si l'utilisateur n'est pas connecté, le rediriger vers la page de connexion
        return redirect('login')

    # Récupérer l'item à supprimer, ou retourner 404 si l'item n'existe pas
    item = get_object_or_404(InventoryItem, pk=item_id)

    # Vérifier si l'item appartient à l'utilisateur connecté
    if item.user_id != user_id:
        messages.error(request, "Vous n'êtes pas autorisé à supprimer cet objet.")
        return redirect('inventory_list')

    if request.method == 'POST':
        # Supprimer l'item
        item.delete()
        messages.success(request, "L'objet a été supprimé avec succès.")
        return redirect('inventory_list')

    # Afficher la page de confirmation pour supprimer l'objet
    return render(request, 'App/delete_item.html', {'item': item})
    

# Consommer un objet (diminuer la quantité)
def consume_item(request, item_id):
    # Récupérer l'ID de l'utilisateur depuis la session
    user_id = request.session.get('user_id')

    if not user_id:
        # Rediriger vers la page de connexion si l'utilisateur n'est pas connecté
        return redirect('login')

    # Récupérer l'objet associé à l'utilisateur
    item = get_object_or_404(InventoryItem, id=item_id, user_id=user_id)

    # Vérifier si l'objet est consommable (potion, plante, clé)
    consommables = ['potion', 'plante', 'clé']
    if item.type in consommables:
        if item.quantite > 0:
            item.quantite -= 1
            item.save()
            messages.success(request, f"L'objet {item.nom} a été consommé.", extra_tags='alert-success')
        else:
            messages.error(request, f"L'objet {item.nom} n'a plus de quantité disponible à consommer.", extra_tags='alert-quantity')
    else:
        messages.error(request, f"L'objet {item.nom} ne peut pas être consommé.",extra_tags='alert-danger')

    return redirect('inventory_list')


def create_hero(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  # Redirige si l'utilisateur n'est pas connecté

    user = User.objects.get(pk=user_id)

    if request.method == 'POST':
        form = HeroForm(request.POST)
        if form.is_valid():
            hero = form.save(commit=False)
            hero.user = user
            hero.save()
            return redirect('home')  # Retour à l'accueil après création
    else:
        form = HeroForm()

    return render(request, 'App/create_hero.html', {'form': form})



def choose_hero_for_board(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    
    # Récupérer tous les héros de l'utilisateur
    user = User.objects.get(pk=user_id)
    all_heroes = user.heroes.all()

    if request.method == 'POST':
        hero_id = request.POST.get('hero_id')
        # Vérifier que hero_id appartient bien à l'utilisateur
        hero = get_object_or_404(Hero, pk=hero_id, user=user)
        
        # Stocker en session (ou en BD) le héros sélectionné
        request.session['selected_hero_id'] = hero_id
        
        # Rediriger vers la page de préparation / lancement du jeu
        return redirect('start_board_game')
        #return redirect('board_view')


    return render(request, 'App/choose_hero.html', {
        'heroes': all_heroes
    })

def start_board_game(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    hero_id = request.session.get('selected_hero_id')
    if not hero_id:
        return redirect('choose_hero')

    hero = get_object_or_404(Hero, pk=hero_id, user_id=user_id)
    rpg_hero = hero.to_rpg_hero()
    joueur_principal = Joueur(rpg_hero)

    random_heroes = []
    for i in range(2):
        random_heroes.append(Joueur(RPGHero({
            'name': f"AleaHero{i}",
            'race': Race("Human", Stat({'strength':8,'agility':7,'speed':7})),
            'classe': Classe("Warrior", Stat({'strength':5,'agility':5,'speed':5})),
            'bag': Bag({'sizeMax': 5, 'items': []}),
            'equipment': [],
            'xp': 0,
        })))

    jeu = Jeu(size=20, nb_obstacles=0, nb_etapes=10)
    jeu.ajouter_joueur(joueur_principal)
    for rh in random_heroes:
        jeu.ajouter_joueur(rh)

    # Lancement du jeu => on récupère la liste des logs
    logs = jeu.lancer()  # renvoie logs

    context = {
        'plateau_cases': jeu.plateau.cases,
        'joueurs': jeu.joueurs,
        'logs': logs,  # On passe la liste de logs au template
    }
    return render(request, 'App/board_result.html', context)



"""def board_view(request):
    # Récupérer l'état du jeu depuis la session
    game_data = request.session.get('board_game_state')
    logs = request.session.get('board_game_logs', [])

    if not game_data:
        # Pas d'état => on initialise le Jeu
        jeu = Jeu(size=20, nb_obstacles=0, nb_etapes=10)

        # -- Vérifier si l'utilisateur a choisi un héros avant --
        hero_id = request.session.get('selected_hero_id')
        if hero_id:
            # Charger ce héros Django
            real_hero = get_object_or_404(Hero, pk=hero_id)
            rpg_hero = real_hero.to_rpg_hero()  # -> un Hero(...) côté avatar
            j_principal = Joueur(rpg_hero)
            jeu.ajouter_joueur(j_principal)
        else:
            # Si rien n'a été choisi, on peut créer un héros par défaut :
            default_hero = RPGHero({
                'name': 'HeroSession',
                'race': Race("Elfe", Stat({ 'strength':10, 'agility':10, 'speed':10 })),
                'classe': Classe("Warrior", Stat({'strength':5,'agility':5,'speed':5})),
                'bag': Bag({'sizeMax':5,'items':[]}),
                'equipment': []
            })
            j_defaut = Joueur(default_hero)
            jeu.ajouter_joueur(j_defaut)

        # On peut ajouter un mob ou un autre héros aléatoire
        mob_ennemi = Mobs({
            'name': 'GoblinEnemy',
            'race': Race("Orc", Stat({'strength':8,'agility':5,'speed':5})),
            'classe': Classe("Monster", Stat({'strength':3,'agility':2,'speed':2})),
            'bag': Bag({'sizeMax':0,'items':[]}),
            'equipment': [],
            'type': 'Mob'
        })
        jeu.ajouter_joueur(Joueur(mob_ennemi))

        # Sauvegarder dans la session
        request.session['board_game_state'] = jeu.to_dict()
        request.session['board_game_logs'] = []
        logs = []
    else:
        # Recharger depuis la session
        jeu = Jeu.from_dict(game_data)

    context = {
        'plateau_cases': jeu.plateau.cases,
        'joueurs': jeu.joueurs,
        'logs': logs,
    }
    return render(request, 'App/board.html', context)


def board_next_turn(request):
    game_data = request.session.get('board_game_state')
    logs = request.session.get('board_game_logs', [])

    if not game_data:
        return redirect('board_view')

    jeu = Jeu.from_dict(game_data)

    new_logs = jeu.plateau.run_one_step()
    logs.extend(new_logs)

    # Debug : imprimer dans la console
    print("DEBUG run_one_step logs:", new_logs)

    request.session['board_game_state'] = jeu.to_dict()
    request.session['board_game_logs'] = logs

    return redirect('board_view')
"""