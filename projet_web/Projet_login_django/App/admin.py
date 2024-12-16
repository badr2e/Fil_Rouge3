from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms

from .models import Item, User, Hero

# Formulaire personnalisé pour définir l'XP
class XPForm(forms.Form):
    xp_gain = forms.IntegerField(
        label="Quantité d'XP à ajouter",
        min_value=1,
        required=True
    )

class HeroAdmin(admin.ModelAdmin):
    list_display = ('name', 'race', 'hero_class', 'level', 'xp', 'get_detailed_stats')
    actions = ['redirect_to_add_xp']

    def get_detailed_stats(self, obj):
        """Affiche les stats détaillées dans l'admin."""
        return obj.detailed_stats()

    get_detailed_stats.short_description = 'Statistiques détaillées'

    @admin.action(description="Ajouter de l'XP aux héros (personnalisé)")
    def redirect_to_add_xp(self, request, queryset):
        # Stocker les IDs des héros sélectionnés
        selected = queryset.values_list('id', flat=True)
        return HttpResponseRedirect(f"add_xp/?ids={','.join(map(str, selected))}")

    def get_urls(self):
        """Ajoute une URL personnalisée pour le formulaire XP."""
        urls = super().get_urls()
        custom_urls = [
            path('add_xp/', self.admin_site.admin_view(self.add_xp_view), name='add_xp'),
        ]
        return custom_urls + urls

    def add_xp_view(self, request):
        """Vue personnalisée pour ajouter de l'XP."""
        ids = request.GET.get('ids', '').split(',')
        heroes = Hero.objects.filter(id__in=ids)

        if request.method == 'POST':
            form = XPForm(request.POST)
            if form.is_valid():
                xp_gain = form.cleaned_data['xp_gain']
                for hero in heroes:
                    hero.level_up(xp_gain=xp_gain)
                self.message_user(request, f"{len(heroes)} héros mis à jour avec {xp_gain} XP.")
                return HttpResponseRedirect("../")
        else:
            form = XPForm()

        return render(request, 'admin/add_xp.html', {'form': form, 'heroes': heroes})


# Enregistrement des modèles
admin.site.register(User)
admin.site.register(Item)
admin.site.register(Hero, HeroAdmin)
