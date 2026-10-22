# X-Burst - Beyblade X Tournament Platform (IAB207 A2)

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
