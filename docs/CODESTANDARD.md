# Code standard — FlaskFirstApp

This document describes the conventions that the code in this project already follows.
It is descriptive, not aspirational: every rule below is taken from existing code, and the
examples point at real files.

Companion document: [ADD-NEW-FEATURE.md](ADD-NEW-FEATURE.md) — a step-by-step recipe for adding a feature.

---

## 1. Architecture — three layers

The project uses a classic 3-layer architecture. Each layer only talks to the layer directly
below it, and never skips a layer.

```
  Browser
     |
     v
  Presentation      app.py  +  templates/*.html        (Flask routes + Jinja2)
     |
     v
  Business logic    services/*.py                      (rules, calculations, orchestration)
     |
     v
  Data access       storage/db_*.py                    (SQLite CRUD)
     |
     v
  SQLite            storage/database/StandingDB.db

  Shared:           models/*.py                        (plain data classes, used by all layers)
```

### Rules

| Rule | Why |
| --- | --- |
| `app.py` never imports `sqlite3` and never imports from `storage/` | Routes must not know how data is stored |
| `services/` never imports `flask`, never touches `request` or `render_template` | Business logic must be testable without a web server |
| `storage/` never imports from `services/` | Data access is the bottom layer; it only knows models |
| `models/` imports nothing from the other layers (except other models) | Models are the shared vocabulary |
| Templates only read from objects handed to them by the route | No logic in the view beyond loops, `if` and formatting |

The one accepted exception: [standing.py](../models/standing.py) inherits from `Team` and `Result`,
so a model may import another model.

---

## 2. Folder and file naming

| Folder | File name pattern | Example |
| --- | --- | --- |
| `models/` | `<singular_noun>.py` | [player.py](../models/player.py), [tournament_match.py](../models/tournament_match.py) |
| `services/` | `<singular_noun>_service.py` | [player_service.py](../services/player_service.py) |
| `storage/` | `db_<plural_noun>.py` | [db_players.py](../storage/db_players.py) |
| `templates/` | `<plural_noun>/<page>.html` | [create-player.html](../templates/players/create-player.html) |
| `tests/` | `test_<model>.py` | [test_player.py](../tests/test_player.py) |

- Python files: `snake_case`.
- HTML template files: `kebab-case` (`create-player.html`, `edit-tournament.html`).
- The list page is named after its folder: `players/players.html`, `teams/teams.html`.

---

## 3. Naming inside the code

| Element | Convention | Example |
| --- | --- | --- |
| Model class | `PascalCase`, singular | `Player`, `TournamentMatch` |
| Service class | `PascalCase` + `Service` | `PlayerService`, `TournamentService` |
| Storage class | `Storage_<Singular>` (deliberate underscore) | `Storage_Player`, `Storage_Team` |
| Method / function | `snake_case` | `get_player_by_id` |
| Private field | `self.__name` (double underscore) | `self.__storage` |
| Private method | `__name` | `__generate_round_robin_schedule` |
| SQL constant | `UPPER_SNAKE_CASE` ending in `_SQL` | `SELECT_BY_ID_SQL` |
| Database table | `PascalCase`, plural | `Players`, `TournamentMatches` |
| Database column | `PascalCase` | `TeamId`, `JerseyNumber` |
| Route function | `snake_case`, matches the action | `create_player`, `edit_tournament` |
| Form field name | `snake_case`, matches the model property | `first_name`, `jersey_number` |

Note the deliberate mismatch: **Python is `snake_case`, SQL is `PascalCase`.** Do not rename
columns to match Python — the mapping happens in the storage layer.

---

## 4. Models (`models/`)

A model is a plain class with private fields exposed through `@property`.

```python
class Player:
    def __init__(self, id, team_id, first_name, last_name, position, jersey_number):
        self.__id = id
        self.__team_id = team_id
        # ...

    @property
    def id(self):
        return self.__id            # id has NO setter - it is assigned by the database

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, new_first_name):
        self.__first_name = new_first_name
```

Rules:

1. All fields are private (`self.__field`).
2. Every field gets a `@property` getter.
3. Every field gets a setter **except `id`**, and except foreign keys that must not change after
   creation — see [tournament_team.py](../models/tournament_team.py) and
   [tournament_match.py](../models/tournament_match.py), where only score and status are settable.
4. The setter parameter is named `new_<field>`.
5. The constructor parameter order **must match the column order of the table**, because storage
   builds models with `Model(*row)`. Getting this wrong silently shifts every value.
6. No database code, no Flask code, no validation logic in a model.
7. Add `to_json()` only if the model is exposed through the JSON API — see `Standing.to_json()`
   in [standing.py](../models/standing.py).

---

## 5. Data access (`storage/`)

One class per table group, constructed with no arguments, opening its own connection.

```python
class Storage_Player:
    SELECT_ALL_SQL   = "SELECT * FROM Players"
    SELECT_BY_ID_SQL = SELECT_ALL_SQL + " WHERE Id = (?)"
    INSERT_SQL       = "INSERT INTO Players(TeamId, FirstName, ...) VALUES(?, ?, ...)"
    UPDATE_SQL       = "UPDATE Players SET TeamId = (?), ... WHERE Id = (?)"
    DELETE_SQL       = "DELETE FROM Players WHERE Id = (?)"

    def __init__(self):
        self.__connection = sqlite3.connect("storage/database/StandingDB.db", check_same_thread=False)
        self.__create_table_if_missing()
```

Rules:

1. **Always parameterised SQL** — `(?)` placeholders and a tuple of values. Never build SQL by
   concatenating or interpolating user input. (A few lines in [db_teams.py](../storage/db_teams.py)
   carry an `f"..."` prefix on a *constant* string; the values are still passed as parameters. Do
   not copy the `f` prefix — it serves no purpose and invites a real injection later.)
2. SQL lives in `UPPER_SNAKE_CASE` class constants at the top of the class. This is the newer
   style ([db_players.py](../storage/db_players.py), [db_results.py](../storage/db_results.py));
   prefer it over inline SQL strings.
3. The connection string is the literal `"storage/database/StandingDB.db"` with
   `check_same_thread=False` (the Flask dev server serves requests on several threads).
4. Rows become models with `Model(*row)`.
5. `add_*` returns `cur.lastrowid` so the service can learn the generated id.
6. `self.__connection.commit()` after every INSERT / UPDATE / DELETE.
7. `cur.close()` when the cursor is finished with.
8. New tables are created defensively with `CREATE TABLE IF NOT EXISTS` in a private
   `__create_table_if_missing()` / `__create_tables()` called from `__init__` — see
   [db_players.py](../storage/db_players.py) and [db_tournaments.py](../storage/db_tournaments.py).
   The same DDL also goes into [sql-create-standing](../storage/SQL_Scripts/sql-create-standing)
   so a fresh database can be built from the script.
9. Storage does no business logic — no sorting rules, no defaults, no validation.

### Standard method set

```
get_all_<plural>()          -> list[Model]
get_<singular>_by_id(id)    -> Model
get_<plural>_by_<fk>(fk)    -> list[Model]     (optional)
add_<singular>(model)       -> int (new id)
update_<singular>(model)    -> None
delete_<singular>(id)       -> None
```

---

## 6. Business logic (`services/`)

```python
class PlayerService:
    def __init__(self):
        self.__storage = Storage_Player()

    def get_all_players(self):
        """
        Getting all players from storage
        """
        return self.__storage.get_all_players()

    def create_player(self, teamid, first_name, last_name, position, jersey_number):
        """
        Creating player and adding to storage
        """
        player = Player(None, teamid, first_name, last_name, position, jersey_number)
        created_id = self.__storage.add_player(player)
        return Player(created_id, teamid, first_name, last_name, position, jersey_number)
```

Rules:

1. The service owns its storage object in `self.__storage` — created in `__init__`, never passed in.
2. Services take and return **models and primitives**, never database rows, never `request.form`.
3. `create_*` builds the model with `id = None`, calls `add_*`, and returns a model carrying the
   new id.
4. Every public method has a short `"""docstring"""` in the present-participle style already in use:
   *"Getting all players from storage"*, *"Creating result and adding to storage"*.
5. Cross-entity work happens by **passing the other service in as an argument**, not by importing
   it. See `TeamService.create_team(..., result_service)` and
   `StandingsService.get_stadings_local(team_service, result_service)`. This keeps services free of
   circular imports.
6. Return type hints are used where the return is a list of models:
   `def get_stadings_us(self) -> list[Standing]:`.
7. `create_some_*()` seed helpers are a project convention for demo data — see
   `TeamService.create_some_objects` and `PlayerService.create_some_players`.

---

## 7. Presentation — routes ([app.py](../app.py))

All routes live in the single file `app.py`. Services are instantiated once at module level:

```python
team_service = TeamService()
player_service = PlayerService()
```

### Route layout

Sections are separated by a full-width comment banner:

```python
#------------------------------------------------------------------------------------------------------------------------------
# Tournament management
#------------------------------------------------------------------------------------------------------------------------------
```

### URL patterns

| Action | URL | Methods |
| --- | --- | --- |
| List | `/<plural>` | GET |
| Create | `/<plural>/create` | GET, POST |
| Edit | `/<plural>/<int:id>/edit` | GET, POST |
| Delete | `/<plural>/<int:id>/delete` | GET |
| Sub-action | `/<plural>/<int:id>/<verb>` | GET or POST |

### Handler shape

Create and edit are each one function with a `request.method` branch:

```python
@app.route('/players/<int:id>/edit', methods=['GET', 'POST'])
def edit_player(id):
    if request.method == "POST":
        player_service.update_player(
            id,
            int(request.form['teamid']),
            request.form['first_name'],
            ...
        )
        return redirect(url_for("players"))
    else:
        return render_template('players/edit-player.html', title = 'Rediger spiller',
                               player = player_service.get_player_by_id(id),
                               teams = team_service.get_all_teams())
```

Rules:

1. A POST always ends in `redirect(url_for(...))` — never render a template after a POST
   (post/redirect/get, so refreshing the browser does not re-submit).
2. Use `url_for("<route function name>")`, not a hard-coded path.
3. Numeric form fields are converted in the route: `int(request.form['teamid'])`. The service
   receives correct types.
4. Every `render_template` passes `title = '<Danish text>'`; the layout renders it in `<title>`
   and as the page `<h2>`.
5. Keyword arguments to `render_template` are named exactly as the template expects them.
6. Routes contain no database loops and no calculations — with the accepted exception of small
   view-model dictionaries such as `tournament_teams_count` and `team_lookup` in `tournaments()`
   and `edit_tournament()`.
7. Docstrings are added to non-obvious routes only (`standingslocal`, `add_win_team`).
8. Delete is a plain GET link guarded by a JavaScript `confirm()` in the template.

---

## 8. Presentation — templates (`templates/`)

Every page extends the single layout:

```jinja
{% extends 'layout.html' %}
{% block content %}
    ...
{% endblock %}
```

Rules:

1. [layout.html](../templates/layout.html) holds `<head>`, the Bootstrap 5.3.8 CDN link,
   `/static/style.css` and the navbar. New top-level features get a `nav-item nav-link` entry there.
2. Styling is Bootstrap classes (`table`, `form-control`, `btn btn-outline-primary`, `col-4`).
   [style.css](../static/style.css) is for the few things Bootstrap does not cover.
3. **All user-facing text is Danish.** Code, comments, docstrings and identifiers are English.
4. On list pages, the **Id cell is the link to the edit page**:
   `<td><a href='/players/{{p.id}}/edit'>{{p.id}}</a></td>`.
5. Forms: `<form action="#" method="post">` inside `<div class="col-4">`, inputs wrapped in
   `<div class="form-group">`, with `<label for="x">`, `name="x"` and `id="x"` all matching the
   `request.form['x']` key used in the route.
6. Create forms pre-fill sensible demo values (`value="John"`, `value="2026"`) so the app is quick
   to try out. Edit forms fill from the model (`value="{{player.first_name}}"`), with the `id`
   field `readonly`.
7. Delete uses the confirm-script pattern from
   [edit-player.html](../templates/players/edit-player.html):

```html
<input type="button" class="btn btn-outline-danger form-control" value="Delete"
       onclick="return confirmdelete({{player.id}})">
<script>
    function confirmdelete(playerid) {
        deleteconfirmed = confirm('Er du sikkert på at du vil slette spilleren?');
        if (deleteconfirmed == true) {
            window.location.href = '/players/' + playerid + '/delete';
        } else {
            return false;
        }
    }
</script>
```

8. Loop variables are short in the older templates (`{% for t in teams %}`) and spelled out in the
   newer ones (`{% for tournament in tournaments %}`). Prefer the spelled-out form.

---

## 9. Tests (`tests/`)

Tests use the standard-library `unittest`, one file per model.

```python
import unittest
from models.player import Player


class TestPlayerModel(unittest.TestCase):
    def test_initial_values(self):
        player = Player(id=10, team_id=42, first_name='John', last_name='Doe',
                        position='Pitcher', jersey_number=7)
        self.assertEqual(player.id, 10)
        ...

    def test_first_name_setter_updates_value(self):
        player = Player(id=1, team_id=2, first_name='Jane', last_name='Smith',
                        position='Catcher', jersey_number=12)
        player.first_name = 'Anna'
        self.assertEqual(player.first_name, 'Anna')


if __name__ == "__main__":
    unittest.main()
```

Rules:

1. Class name `Test<Model>Model`; method names `test_<what>_<expected>`.
2. The constructor is called with **keyword arguments** — this is what makes the test double as a
   check that parameter names have not drifted.
3. One `test_initial_values` covering the constructor, then one test per setter.
4. Models are tested in isolation — no database, no Flask, no mocks needed.
5. Run from the project root so the `models` package resolves:

```
python -m unittest discover -s tests -t .
```

---

## 10. Git

- Branch off `main`, one branch per feature, named after the feature
  (`Creating-SQL-View---InProc` is an existing example).
- Commit messages are short and describe the feature: `add unit test player for model`,
  `Turnement create`, `Player administration added`.
- `storage/database/StandingDB.db` is in [.gitignore](../.gitignore) — **the database is never
  committed.** A schema change must therefore go into both
  [sql-create-standing](../storage/SQL_Scripts/sql-create-standing) *and* a
  `CREATE TABLE IF NOT EXISTS` in the storage class, or the feature will not work on another machine.

---

## 11. Known deviations — do not copy these

These exist in the code today but are **not** the standard. Fix them if you touch the file.

| File | Issue |
| --- | --- |
| [db_standing.py](../storage/db_standing.py) | The class is named `Storage_Result` (copy/paste from `db_results.py`) and `Standing(row[0], 'N/A', 1, )` does not match the `Standing` constructor. The file is unused. |
| [test_team.py](../tests/test_team.py) | Constructs `Team(id=, name=, wins=, losses=)`, but `Team.__init__` takes `(id, season, city, name, league, division)`. This test cannot pass. |
| [tournament_service.py](../services/tournament_service.py) | `normalized_format = 'Round robin' if ... else 'Round robin' if ... else 'Round robin'` — all three branches yield the same value. |
| [stadings_service.py](../services/stadings_service.py) | The filename is misspelled (`stadings`), the API key is hard-coded in the source, and `standings.sort(...)` runs inside the loop instead of after it. |
| [db_results.py](../storage/db_results.py) | `get_result_by_id` / `get_result_by_teamid` raise `UnboundLocalError` when no row matches. Use the `fetchone()` + `if row is None: return None` pattern from [db_tournaments.py](../storage/db_tournaments.py) instead. |

For new code, the reference implementations to copy are the **player** feature
([player.py](../models/player.py) → [db_players.py](../storage/db_players.py) →
[player_service.py](../services/player_service.py) → routes in [app.py](../app.py) →
[templates/players/](../templates/players/)) and, for multi-table features, the **tournament** feature.
