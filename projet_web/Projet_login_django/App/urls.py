from django.urls import path
from django.contrib.auth import views as auth_views
from .views import create_hero




from .views import inventory_list_view, login_view, home_view, signup_view, inventory_list, add_item, update_item, delete_item, consume_item  # Importe les vues définies dans le fichier views.py

# Définition des URL pour l'application. 
# Chaque URL est liée à une vue spécifique qui gère la logique pour cette route.

urlpatterns = [
    path('login/', login_view, name='login'),
    path("", home_view, name="home"),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', signup_view, name='signup'),  # URL pour la page d'inscription
    path('list/', inventory_list, name='inventory_list'),
    path('add/', add_item, name='add_item'),
    path('update/<int:item_id>/', update_item, name='update_item'),
    path('delete/<int:item_id>/', delete_item, name='delete_item'),
    path('consume/<int:item_id>/', consume_item, name='consume_item'),
    path('inventory/', inventory_list_view, name='inventory_list'),
    path('hero/create/', create_hero, name='create-hero'),
]
