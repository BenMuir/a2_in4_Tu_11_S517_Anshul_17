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
The SQLite database is created automatically at `instance/beyblade.sqlite`
the first time the app starts.

If someone changes a model (adds/renames a column), delete `instance/beyblade.sqlite`
and restart the app to rebuild it. `db.create_all()` only creates missing tables;
it does not update existing ones.
