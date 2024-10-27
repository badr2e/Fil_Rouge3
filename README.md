## Créateur

- Michelozzi Matthieu
- Mirande Clémentine


## Prérequis

- Python 3.x
- pip (Python package installer)
- Virtualenv (optionnel mais recommandé)

## Installation

1. Clonez le dépôt :

    ```sh
    git clone <https://github.com/Michelozzi2/Projet_web.git>
    cd projet_web/Projet_login_django
    ```

2. Créez un environnement virtuel (optionnel mais recommandé) :

    ```sh
    python -m venv env
    source env/bin/activate  # Sur Windows, utilisez `env\Scripts\activate`
    ```

3. Installez les dépendances :

    ```sh
    pip install -r requirements.txt
    ```

4. Appliquez les migrations de la base de données :

    ```sh
    python manage.py migrate
    ```

5. Créez un superutilisateur pour accéder à l'admin Django :

    ```sh
    python manage.py createsuperuser
    ```

6. Lancez le serveur de développement :

    ```sh
    python manage.py runserver
    ```

7. Accédez à l'application dans votre navigateur à l'adresse `http://127.0.0.1:8000/`.

## Structure des dossiers

- `App/` : Contient les fichiers de l'application principale.
- `migrations/` : Contient les fichiers de migration de la base de données.
- `static/` : Contient les fichiers statiques (CSS, JavaScript, images).
- `templates/` : Contient les templates HTML.
- `db.sqlite3` : Fichier de base de données SQLite.
- `manage.py` : Script de gestion de Django.
- `Projet_login_django/` : Contient les fichiers de configuration du projet Django.

## Fonctionnalités

- Gestion des utilisateurs (inscription, connexion, déconnexion).
- Interface d'administration pour gérer les utilisateurs et les données.

## Contribuer

Les contributions sont les bienvenues ! Veuillez soumettre une pull request ou ouvrir une issue pour discuter des changements que vous souhaitez apporter.

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.