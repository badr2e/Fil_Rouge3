from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .forms import ItemForm, SignUpForm
from .models import Item, User
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from .forms import HeroForm
from .models import Hero
from django.contrib.auth.models import AnonymousUser  # Import pour tester l'état de connexion




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
    items = Item.objects.filter(user_id=user_id)

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
    item = get_object_or_404(Item, id=item_id, user_id=user_id)

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
    item = get_object_or_404(Item, pk=item_id)

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
    item = get_object_or_404(Item, id=item_id, user_id=user_id)

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

