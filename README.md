# Django Starter App

Lauffähiges Django-Beispielprojekt mit drei Apps:

- `main` als Rahmen-App
- `auth_app` für Registrierung, Login, Logout und Passwort-Reset
- `todo` als geschützte To-do-App

## Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Dann im Browser öffnen:

- Startseite: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`
- Login: `http://127.0.0.1:8000/auth/login/`
- Registrierung: `http://127.0.0.1:8000/auth/register/`
- Todos: `http://127.0.0.1:8000/todos/`

## Enthaltene Funktionen

### main
- einfache Startseite
- Basislayout
- Navigation

### auth_app
- Benutzerregistrierung
- Login / Logout
- Passwort-Reset-Views
- vorbereitet für spätere Erweiterungen wie Profile, Rollen, E-Mail-Verifizierung

### todo
- To-do-Liste pro Benutzer
- Erstellen
- Bearbeiten
- Löschen
- Status umschalten

## Nächste sinnvolle Erweiterungen

- eigenes Custom-User-Modell
- E-Mail-Verifizierung
- Rollen und Gruppen
- Permission-Mixins / Decorators
- API mit Django REST Framework
- Tests mit `pytest` oder Django TestCase

