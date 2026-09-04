# How to add a new feature

A step-by-step recipe for adding a new CRUD feature to FlaskFirstApp, following the conventions in
[CODESTANDARD.md](CODESTANDARD.md).

The worked example throughout is a **Coach** feature (Danish UI: *Trænere*) — a coach belongs to a
team and has a first name, last name, role and the year they were hired. Replace `Coach` / `coach` /
`coaches` / `Coaches` with your own entity.

---

## 0. Before you start

```powershell
git checkout main
git pull
git checkout -b Coach-administration
```

Check that the app runs and the database exists:

```powershell
python app.py
```

The database file `storage/database/StandingDB.db` is **not** in git. If you do not have it, create
it with the DDL in [sql-create-standing](../storage/SQL_Scripts/sql-create-standing) — see
[storage/SQL_Scripts/readme.txt](../storage/SQL_Scripts/readme.txt).

---

## The order of work

Build **bottom-up**. Each step compiles and can be checked before you move on.

```
  1. Database table        SQL script + CREATE TABLE IF NOT EXISTS
  2. Model                 models/coach.py
  3. Storage               storage/db_coaches.py
  4. Service               services/coach_service.py
  5. Routes                app.py
  6. Templates             templates/coaches/*.html
  7. Navigation            templates/layout.html
  8. Test                  tests/test_coach.py
  9. Run and commit
```

Do not start with the HTML. The template is the last thing that can be written, because it depends
on names decided in every layer below it.

---

## Step 1 — Database table

Decide the columns first. **The column order fixes the constructor order of the model**, because
storage builds models with `Model(*row)`.

| Column | Type | Note |
| --- | --- | --- |
| `Id` | INTEGER PRIMARY KEY AUTOINCREMENT | always first |
| `TeamId` | INTEGER NOT NULL | foreign key |
| `FirstName` | VARCHAR(50) | |
| `LastName` | VARCHAR(50) | |
| `Role` | VARCHAR(30) | |
| `HiredYear` | INTEGER | |

Append the table to [storage/SQL_Scripts/sql-create-standing](../storage/SQL_Scripts/sql-create-standing):

```sql
CREATE TABLE Coaches(
	Id INTEGER PRIMARY KEY AUTOINCREMENT,
	TeamId INTEGER NOT NULL,
	FirstName VARCHAR(50),
	LastName VARCHAR(50),
	Role VARCHAR(30),
	HiredYear INTEGER,
	FOREIGN KEY (TeamId) REFERENCES Teams(Id)
);
```

You will add the same table again as `CREATE TABLE IF NOT EXISTS` in step 3, so that the feature
also works on a machine where the database already exists. Both are required — the `.db` file is
gitignored, so the SQL script is the only record of the schema in the repository.

---

## Step 2 — Model

Create `models/coach.py`. Private fields, a getter for everything, a setter for everything except
`id`, and the constructor order matching the table.

```python
class Coach:
    def __init__(self, id, team_id, first_name, last_name, role, hired_year):
        self.__id = id
        self.__team_id = team_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__role = role
        self.__hired_year = hired_year

    @property
    def id(self):
        return self.__id

    @property
    def teamid(self):
        return self.__team_id

    @teamid.setter
    def teamid(self, new_team_id):
        self.__team_id = new_team_id

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, new_first_name):
        self.__first_name = new_first_name

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, new_last_name):
        self.__last_name = new_last_name

    @property
    def role(self):
        return self.__role

    @role.setter
    def role(self, new_role):
        self.__role = new_role

    @property
    def hired_year(self):
        return self.__hired_year

    @hired_year.setter
    def hired_year(self, new_hired_year):
        self.__hired_year = new_hired_year
```

Note the existing quirk worth keeping for consistency: the constructor parameter is `team_id`, but
the property is `teamid` (same as in [player.py](../models/player.py) and
[result.py](../models/result.py)).

---

## Step 3 — Storage

Create `storage/db_coaches.py`. Copy [db_players.py](../storage/db_players.py) — it is the
reference implementation.

```python
import sqlite3
from models.coach import Coach


class Storage_Coach:
    SELECT_ALL_SQL = "SELECT * FROM Coaches"
    SELECT_BY_ID_SQL = SELECT_ALL_SQL + " WHERE Id = (?)"
    SELECT_BY_TEAMID_SQL = SELECT_ALL_SQL + " WHERE TeamId = (?)"
    INSERT_SQL = "INSERT INTO Coaches(TeamId, FirstName, LastName, Role, HiredYear) VALUES(?, ?, ?, ?, ?)"
    UPDATE_SQL = "UPDATE Coaches SET TeamId = (?), FirstName = (?), LastName = (?), Role = (?), HiredYear = (?) WHERE Id = (?)"
    DELETE_SQL = "DELETE FROM Coaches WHERE Id = (?)"

    def __init__(self):
        self.__connection = sqlite3.connect("storage/database/StandingDB.db", check_same_thread=False)
        self.__create_table_if_missing()

    def __create_table_if_missing(self):
        cur = self.__connection.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS Coaches(
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                TeamId INTEGER NOT NULL,
                FirstName VARCHAR(50),
                LastName VARCHAR(50),
                Role VARCHAR(30),
                HiredYear INTEGER,
                FOREIGN KEY (TeamId) REFERENCES Teams(Id)
            )
            """
        )
        self.__connection.commit()
        cur.close()

    def get_all_coaches(self):
        cur = self.__connection.cursor()
        cur.execute(self.SELECT_ALL_SQL)
        coaches = []
        for row in cur:
            coaches.append(Coach(*row))
        cur.close()
        return coaches

    def get_coach_by_id(self, id):
        cur = self.__connection.cursor()
        cur.execute(self.SELECT_BY_ID_SQL, (id,))
        row = cur.fetchone()
        cur.close()
        if row is None:
            return None
        return Coach(*row)

    def get_coaches_by_teamid(self, teamid):
        cur = self.__connection.cursor()
        cur.execute(self.SELECT_BY_TEAMID_SQL, (teamid,))
        coaches = []
        for row in cur:
            coaches.append(Coach(*row))
        cur.close()
        return coaches

    def add_coach(self, coach: Coach):
        cur = self.__connection.cursor()
        cur.execute(
            self.INSERT_SQL,
            (coach.teamid, coach.first_name, coach.last_name, coach.role, coach.hired_year),
        )
        self.__connection.commit()
        return cur.lastrowid

    def update_coach(self, coach: Coach):
        cur = self.__connection.cursor()
        cur.execute(
            self.UPDATE_SQL,
            (coach.teamid, coach.first_name, coach.last_name, coach.role, coach.hired_year, coach.id),
        )
        self.__connection.commit()
        cur.close()

    def delete_coach(self, id):
        cur = self.__connection.cursor()
        cur.execute(self.DELETE_SQL, (id,))
        self.__connection.commit()
        cur.close()
```

Checklist for this file:

- [ ] Class named `Storage_Coach`.
- [ ] All SQL in `_SQL` constants, all values passed as `(?)` parameters — never string-formatted in.
- [ ] `Id` is **not** in the `INSERT` column list; SQLite generates it.
- [ ] `add_coach` returns `cur.lastrowid`.
- [ ] `commit()` after insert/update/delete, `cur.close()` when done.
- [ ] Nothing here decides business rules.

---

## Step 4 — Service

Create `services/coach_service.py`. Copy [player_service.py](../services/player_service.py).

```python
from models.coach import Coach
from storage.db_coaches import Storage_Coach


class CoachService:
    def __init__(self):
        self.__storage = Storage_Coach()

    def get_all_coaches(self):
        """
        Getting all coaches from storage
        """
        return self.__storage.get_all_coaches()

    def get_coach_by_id(self, id):
        """
        Getting coach by id from storage
        """
        return self.__storage.get_coach_by_id(id)

    def get_coaches_by_teamid(self, teamid):
        """
        Getting all coaches for a team
        """
        return self.__storage.get_coaches_by_teamid(teamid)

    def create_coach(self, teamid, first_name, last_name, role, hired_year):
        """
        Creating coach and adding to storage
        """
        coach = Coach(None, teamid, first_name, last_name, role, hired_year)
        created_id = self.__storage.add_coach(coach)
        return Coach(created_id, teamid, first_name, last_name, role, hired_year)

    def update_coach(self, id, teamid, first_name, last_name, role, hired_year):
        """
        Updating coach in storage
        """
        coach = Coach(id, teamid, first_name, last_name, role, hired_year)
        self.__storage.update_coach(coach)
        return coach

    def delete_coach(self, id):
        """
        Deleting coach from storage
        """
        self.__storage.delete_coach(id)
```

**Where the business rules go.** Anything that is not "read/write a row" belongs here, not in the
route and not in storage. Examples of rules that would live in `CoachService`:

- only one coach per team may have the role *Head coach*;
- `hired_year` may not be later than the current season;
- deleting a team also deletes its coaches.

If a rule needs another entity, take that service as an argument rather than importing it — the same
way `TeamService.create_team(..., result_service)` creates an empty result row when a team is
created:

```python
def create_coach(self, teamid, first_name, last_name, role, hired_year, team_service):
    team = team_service.get_team_by_id(teamid)
    if team is None:
        return None
    ...
```

---

## Step 5 — Routes

In [app.py](../app.py):

**5a.** Import and instantiate the service at the top, next to the others:

```python
from services.coach_service import CoachService
...
coach_service = CoachService()
```

**5b.** Add a section banner and the four routes. Place the section after the related ones (coaches
belong with the local-league administration):

```python
#------------------------------------------------------------------------------------------------------------------------------
# Coach administration
#------------------------------------------------------------------------------------------------------------------------------
@app.route('/coaches')
def coaches():
    return render_template('coaches/coaches.html', title = 'Trænere',
                           coaches = coach_service.get_all_coaches())

@app.route('/coaches/create', methods=['GET', 'POST'])
def create_coach():
    if request.method == "POST":
        coach_service.create_coach(
            int(request.form['teamid']),
            request.form['first_name'],
            request.form['last_name'],
            request.form['role'],
            int(request.form['hired_year'])
        )
        return redirect(url_for("coaches"))
    else:
        return render_template('coaches/create-coach.html', title = 'Opret træner',
                               teams = team_service.get_all_teams())

@app.route('/coaches/<int:id>/edit', methods=['GET', 'POST'])
def edit_coach(id):
    if request.method == "POST":
        coach_service.update_coach(
            id,
            int(request.form['teamid']),
            request.form['first_name'],
            request.form['last_name'],
            request.form['role'],
            int(request.form['hired_year'])
        )
        return redirect(url_for("coaches"))
    else:
        return render_template('coaches/edit-coach.html', title = 'Rediger træner',
                               coach = coach_service.get_coach_by_id(id),
                               teams = team_service.get_all_teams())

@app.route('/coaches/<int:id>/delete')
def delete_coach(id):
    coach_service.delete_coach(id)
    return redirect(url_for("coaches"))
```

Checklist for the routes:

- [ ] URL pattern is `/coaches`, `/coaches/create`, `/coaches/<int:id>/edit`, `/coaches/<int:id>/delete`.
- [ ] Create and edit are one function each with an `if request.method == "POST":` branch.
- [ ] Every POST branch ends in `redirect(url_for(...))` — never a `render_template`.
- [ ] Numbers are converted with `int(...)` **in the route**.
- [ ] Every `render_template` passes a Danish `title`.
- [ ] The dropdown of teams comes from `team_service` — a route may use several services.
- [ ] No `sqlite3`, no SQL, no rules in `app.py`.

---

## Step 6 — Templates

Create the folder `templates/coaches/` with three files.

### 6a. `templates/coaches/coaches.html` — the list

```jinja
{% extends 'layout.html' %}
{% block content %}
    <p>&nbsp;</p>
    <table class="table">
    <thead>
        <tr>
            <th>Id</th>
            <th>Hold id</th>
            <th>Fornavn</th>
            <th>Efternavn</th>
            <th>Rolle</th>
            <th>Ansat år</th>
        </tr>
    </thead>
    <tbody>
    {% for coach in coaches %}
        <tr>
            <td><a href='/coaches/{{coach.id}}/edit'>{{coach.id}}</a></td>
            <td>{{coach.teamid}}</td>
            <td>{{coach.first_name}}</td>
            <td>{{coach.last_name}}</td>
            <td>{{coach.role}}</td>
            <td>{{coach.hired_year}}</td>
        </tr>
    {% endfor %}
    </tbody>
    </table>
    <p>&nbsp;</p>
    Opret en ny træner - <a href="/coaches/create">opret træner</a>
    <br><br>
    <hr>
    <a href="/teams">Gå tilbage til holdadministration</a>
{% endblock %}
```

### 6b. `templates/coaches/create-coach.html`

```jinja
{% extends 'layout.html' %}
{% block content %}
    <div class="col-4">
        <form action="#" method="post">
            <div class="form-group">
                <label for="teamid">Hold:</label>
                <select name="teamid" id="teamid" class="form-control" required>
                    {% for team in teams %}
                        <option value="{{team.id}}">{{team.name}} ({{team.city}})</option>
                    {% endfor %}
                </select>

                <label for="first_name">Fornavn:</label>
                <input type="text" name="first_name" id="first_name" class="form-control" value="John" required>

                <label for="last_name">Efternavn:</label>
                <input type="text" name="last_name" id="last_name" class="form-control" value="Doe" required>

                <label for="role">Rolle:</label>
                <select name="role" id="role" class="form-control" required>
                    <option selected value="Head coach">Head coach</option>
                    <option value="Assistant coach">Assistant coach</option>
                    <option value="Pitching coach">Pitching coach</option>
                </select>

                <label for="hired_year">Ansat år:</label>
                <input type="number" name="hired_year" id="hired_year" class="form-control" value="2026" required>

                <br>
                <input type="submit" class="form-control" value="Opret træner">
            </div>
        </form>
    </div>
{% endblock %}
```

### 6c. `templates/coaches/edit-coach.html`

```jinja
{% extends 'layout.html' %}
{% block content %}
    <div class="col-4">
        <form action="#" method="post">
            <div class="form-group">
                <label for="id">Id:</label>
                <input type="number" name="id" id="id" class="form-control" readonly value="{{coach.id}}">

                <label for="teamid">Hold:</label>
                <select name="teamid" id="teamid" class="form-control" required>
                    {% for team in teams %}
                        <option value="{{team.id}}" {% if team.id == coach.teamid %}selected{% endif %}>{{team.name}} ({{team.city}})</option>
                    {% endfor %}
                </select>

                <label for="first_name">Fornavn:</label>
                <input type="text" name="first_name" id="first_name" class="form-control" value="{{coach.first_name}}" required>

                <label for="last_name">Efternavn:</label>
                <input type="text" name="last_name" id="last_name" class="form-control" value="{{coach.last_name}}" required>

                <label for="role">Rolle:</label>
                <input type="text" name="role" id="role" class="form-control" value="{{coach.role}}" required>

                <label for="hired_year">Ansat år:</label>
                <input type="number" name="hired_year" id="hired_year" class="form-control" value="{{coach.hired_year}}" required>

                <br>
                <input type="submit" class="btn btn-outline-primary form-control" value="Update"><br><br>
                <input type="button" class="btn btn-outline-danger form-control" value="Delete" onclick="return confirmdelete({{coach.id}})">
            </div>
        </form>
    </div>
    <script>
        function confirmdelete(coachid) {
            deleteconfirmed = confirm('Er du sikkert på at du vil slette træneren?');
            if (deleteconfirmed == true) {
                window.location.href = '/coaches/' + coachid + '/delete';
            } else {
                return false;
            }
        }
    </script>
{% endblock %}
```

Checklist for the templates:

- [ ] Each file starts with `{% extends 'layout.html' %}` and wraps everything in
      `{% block content %}`.
- [ ] Every `name="x"` matches a `request.form['x']` in the route, and matches the model property.
- [ ] All visible text is Danish.
- [ ] Bootstrap classes only; no inline `style=` attributes.
- [ ] The Id column on the list page links to the edit page.
- [ ] Delete goes through the `confirmdelete` script.

---

## Step 7 — Navigation

Add the entry to the navbar in [templates/layout.html](../templates/layout.html), in the same order
as the app flow:

```html
<a class="nav-item nav-link" href="/coaches">Træner administration</a>
```

---

## Step 8 — Test

Create `tests/test_coach.py`, following [test_player.py](../tests/test_player.py): one test for the
constructor, one per setter, constructed with keyword arguments.

```python
import unittest

from models.coach import Coach


class TestCoachModel(unittest.TestCase):
    def test_initial_values(self):
        coach = Coach(id=10, team_id=42, first_name='John', last_name='Doe',
                      role='Head coach', hired_year=2026)

        self.assertEqual(coach.id, 10)
        self.assertEqual(coach.teamid, 42)
        self.assertEqual(coach.first_name, 'John')
        self.assertEqual(coach.last_name, 'Doe')
        self.assertEqual(coach.role, 'Head coach')
        self.assertEqual(coach.hired_year, 2026)

    def test_teamid_setter_updates_value(self):
        coach = Coach(id=1, team_id=2, first_name='Jane', last_name='Smith',
                      role='Assistant coach', hired_year=2024)

        coach.teamid = 99
        self.assertEqual(coach.teamid, 99)

    def test_role_setter_updates_value(self):
        coach = Coach(id=1, team_id=2, first_name='Jane', last_name='Smith',
                      role='Assistant coach', hired_year=2024)

        coach.role = 'Head coach'
        self.assertEqual(coach.role, 'Head coach')

    def test_hired_year_setter_updates_value(self):
        coach = Coach(id=1, team_id=2, first_name='Jane', last_name='Smith',
                      role='Assistant coach', hired_year=2024)

        coach.hired_year = 2026
        self.assertEqual(coach.hired_year, 2026)


if __name__ == "__main__":
    unittest.main()
```

Run from the project root:

```powershell
python -m unittest discover -s tests -t .
```

If a service method contains a real rule (not just a pass-through to storage), it is worth a test
too — construct the service, call the method, assert on the returned model. Be aware that a service
opens a real SQLite connection in `__init__`, so such a test touches the real database file.

---

## Step 9 — Run it and commit

```powershell
python app.py
```

Then click through the whole flow in the browser:

1. `/coaches` — the list renders, empty is fine.
2. `/coaches/create` — the team dropdown is populated, submit redirects back to the list.
3. Click an Id — the edit form is pre-filled and the correct team is selected.
4. Change a value, press *Update* — the change shows in the list.
5. Press *Delete* — the confirm dialog appears, and the row disappears.
6. The navbar link works from every page.

Commit:

```powershell
git add .
git commit -m "Coach administration added"
git push -u origin Coach-administration
```

Then open a pull request against `main`.

---

## Quick checklist

Copy this into your pull request description:

```
- [ ] Table added to storage/SQL_Scripts/sql-create-standing
- [ ] CREATE TABLE IF NOT EXISTS in the storage class __init__
- [ ] models/<name>.py       - private fields, properties, no setter on id, ctor order = column order
- [ ] storage/db_<names>.py  - Storage_<Name>, _SQL constants, parameterised queries, commit + close
- [ ] services/<name>_service.py - owns its storage, docstrings, all rules live here
- [ ] app.py                 - service instantiated at module level, 4 routes, POST -> redirect
- [ ] templates/<names>/     - list + create + edit, extends layout.html, Danish text
- [ ] layout.html            - navbar entry
- [ ] tests/test_<name>.py   - constructor + one test per setter, all tests pass
- [ ] Clicked through create / edit / delete in the browser
- [ ] No sqlite3 or SQL in app.py; no flask import in services/ or storage/
```

---

## Variations

### A feature that only reads data (no table of its own)

Follow the pattern of [stadings_service.py](../services/stadings_service.py): no storage class, the
service composes data from other services passed in as arguments, and the route just renders it.

### A feature spanning several tables

Follow the tournament pattern: one storage class
([db_tournaments.py](../storage/db_tournaments.py)) owns all three related tables
(`Tournaments`, `TournamentTeams`, `TournamentMatches`), with one model per table, and one service
([tournament_service.py](../services/tournament_service.py)) holding the logic that spans them —
such as `generate_schedule`.

### A JSON endpoint

Follow `/api/standings` in [app.py](../app.py): give the model a `to_json()` method, add a service
method that returns a list of those dictionaries, and return it directly from the route.

```python
@app.route('/api/coaches', methods = ['GET'])
def get_all_coaches_json():
    """
    Exposing coaches as JSON
    """
    return coach_service.get_all_coaches_json()
```
