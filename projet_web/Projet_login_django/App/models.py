from django.db import models

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