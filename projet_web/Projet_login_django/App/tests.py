from django.test import TestCase
from .models import User

class UserModelTests(TestCase):
    
    def setUp(self):
        # Crée un utilisateur pour les tests
        self.user = User.objects.create(
            user_login='testuser',
            user_password='password123',
            user_compte_id=2,  # Assurez-vous d'utiliser une valeur unique
            user_mail='test@example.com'
        )

    def test_user_creation(self):
        """Test de la création d'un utilisateur."""
        self.assertEqual(self.user.user_login, 'testuser')
        self.assertEqual(self.user.user_mail, 'test@example.com')
        self.assertIsNotNone(self.user.user_date_new)  # Vérifie que la date de création est définie
        self.assertIsNotNone(self.user.user_date_login)  # Vérifie que la date de dernière connexion est définie

    def test_user_unique_compte_id(self):
        """Test que le user_compte_id est unique."""
        with self.assertRaises(Exception):  # On s'attend à une exception en raison de la contrainte d'unicité
            User.objects.create(
                user_login='anotheruser',
                user_password='password456',
                user_compte_id=2,  # Utilise le même compte_id que l'utilisateur existant
                user_mail='another@example.com'
            )

    def test_user_str_method(self):
        """Test de la méthode __str__ du modèle User."""
        self.assertEqual(str(self.user), 'testuser')

    def test_user_login(self):
        """Test de la connexion avec des informations valides."""
        user = User.objects.get(user_login='testuser')
        self.assertEqual(user.user_password, 'password123')  # Vérifie le mot de passe

    def test_user_login_invalid(self):
        """Test de la connexion avec des informations invalides."""
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(user_login='nonexistentuser')  # Devrait lever une exception
