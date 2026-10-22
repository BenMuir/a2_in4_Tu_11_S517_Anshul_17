# X-Burst - Beyblade X Tournament Platform (IAB207 A2)

X-Burst is an event management site for local Beyblade X tournaments. Anyone can
browse and search events; registered users can book player slots, comment, and
host their own tournaments with an Acknowledgement of Country.

## Project structure
```
main.py                 Runs the app locally
seed.py                 Resets the database with demo data
requirements.txt
instance/beyblade.sqlite  SQLite database (pre-filled demo data)
beyblade/
  __init__.py           create_app(): config, extensions, blueprints, error pages
  extensions.py         SQLAlchemy, Flask-Login and Bootstrap-Flask objects
  models.py             User, Tournament, Booking, Comment
  forms.py              Flask-WTF forms
  auth.py               Register / login / logout routes
  routes.py             Events, bookings, comments, search
  semantic_search.py    AI search (sentence-transformers, all-MiniLM-L6-v2)
  aoc.py                Acknowledgement of Country guidance (custodians, sources, prompts)
  templates/  static/
```

## Setup (first time)
From this folder (the one containing `main.py`):

```
python -m venv venv
venv\Scripts\python -m pip install -r requirements.txt
```

## Run
```
venv\Scripts\python main.py
```
Then open http://127.0.0.1:5001

## Database
The shared database `instance/beyblade.sqlite` is committed to the repo and comes
pre-filled with demo data (8 tournaments covering every status, bookings and comments).

### Demo accounts
All demo accounts use the password `Blader2026!`

| Email | Role in the demo data |
|---|---|
| demo@example.com | Has confirmed, attended and cancelled bookings |
| sam.nguyen@example.com | Hosts the Brisbane X-Burst Open (can edit/cancel it) |
| priya.sharma@example.com | Hosts West End Friday Night Swiss |
| liam.oconnor@example.com | Hosts Sydney Limited and Canberra Capital Cup |
| mia.thompson@example.com | Hosts Melbourne Casual Spin Meetup |
| jordan.lee@example.com | Hosts Perth Summer Championship (sold out) |

### Resetting the demo data
Testing the site changes the database. To put it back to the clean demo data
(this deletes everything in it):

```
venv\Scripts\python seed.py
```

Run this after anyone changes a model too, since `db.create_all()` only creates
missing tables and does not update existing ones. Re-seed and commit the database
before the final presentation and before submitting, and avoid committing it otherwise -
two people committing different copies causes a merge conflict that git cannot merge.

## AI search
The search page offers Smart search (AI) and Keyword search. Smart search uses the
`all-MiniLM-L6-v2` model from sentence-transformers. It runs locally with no API key;
the model (~90 MB) downloads automatically the first time a search runs.

If sentence-transformers is not installed, Smart search automatically falls back to
keyword search, so the rest of the site works without it.

## Deploying to PythonAnywhere
1. In a PythonAnywhere Bash console, clone the repo and create a virtualenv:
   ```
   git clone https://github.com/BenMuir/a2_in4_Tu_11_S517_Anshul_17.git
   cd a2_in4_Tu_11_S517_Anshul_17
   mkvirtualenv --python=python3.11 xburst-venv
   pip install Flask==3.1.3 Flask-WTF==1.3.0 Flask-SQLAlchemy==3.1.1 Flask-Login==0.6.3 Bootstrap-Flask==2.6.0 Werkzeug==3.1.9 WTForms==3.2.2 SQLAlchemy==2.1.1 email-validator==2.2.0
   ```
   (This skips sentence-transformers, which is too large for the free tier's disk quota.
   Search falls back to keyword matching on the deployed site, which the brief allows.)
2. On the **Web** tab, add a new web app with **Manual configuration** and the same Python version.
3. Set **Source code** and **Working directory** to `/home/<username>/a2_in4_Tu_11_S517_Anshul_17`
   and **Virtualenv** to `xburst-venv`.
4. Edit the **WSGI configuration file** so it contains:
   ```python
   import os, sys
   path = '/home/<username>/a2_in4_Tu_11_S517_Anshul_17'
   if path not in sys.path:
       sys.path.insert(0, path)
   os.environ['SECRET_KEY'] = 'replace-with-a-long-random-string'
   from main import app as application
   ```
5. Under **Static files**, map URL `/static/` to `/home/<username>/a2_in4_Tu_11_S517_Anshul_17/beyblade/static`.
6. Click **Reload** and open `<username>.pythonanywhere.com`.
