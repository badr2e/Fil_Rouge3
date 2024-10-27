from django.contrib import admin  # Importe le module d'administration de Django

from .models import Item, User  # Importe le modèle 'User' défini dans models.py

# Enregistre le modèle 'User' dans l'interface d'administration de Django.
# Cela permet de gérer les objets 'User' via le panneau d'administration.
admin.site.register(User)
admin.site.register(Item)  # Enregistre le modèle 'Item' dans l'interface d'administration