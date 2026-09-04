# Code standard — `<PROJECT_NAME>`

> **This is a template.** It describes a formalised structure for a small/medium Python + Flask web
> application with a SQL database. It is domain-neutral: every place that depends on *what your app
> is about* is written as a `<PLACEHOLDER>`.
>
> Drop this single file into a new project as `docs/CODESTANDARD.md`, fill in
> [§0 Project variables](#0-project-variables), delete this quote block, and the rest of the
> document becomes the code standard for that project.
>
> The document is meant to be **descriptive, not aspirational**: once the first feature is built,
> every rule below should point at real code in your repository. Update it when the code changes.

---

## Table of contents

- [0. Project variables — fill these in first](#0-project-variables)
- [1. Architecture — three layers](#1-architecture--three-layers)
- [2. Folder and file naming](#2-folder-and-file-naming)
- [3. Naming inside the code](#3-naming-inside-the-code)
- [4. Models](#4-models)
- [5. Data access (storage)](#5-data-access-storage)
- [6. Business logic (services)](#6-business-logic-services)
- [7. Presentation — routes](#7-presentation--routes)
- [8. Presentation — templates](#8-presentation--templates)
- [9. Tests](#9-tests)
- [10. Git and branching](#10-git-and-branching)
- [11. Known deviations — do not copy these](#11-known-deviations--do-not-copy-these)
- [12. Recipe — how to add a new feature](#12-recipe--how-to-add-a-new-feature)
- [13. Variations on the recipe](#13-variations-on-the-recipe)
- [14. Adapting this template to a new project](#14-adapting-this-template-to-a-new-project)

---

## 0. Project variables

Fill these in once. Every `<PLACEHOLDER>` in the rest of the document refers back to this table.

| Placeholder | Meaning | Your value |
| --- | --- | --- |
| `<PROJECT_NAME>` | Repository / application name | |
| `<DOMAIN>` | One sentence: what business problem the app solves | |
| `<DB_ENGINE>` | Database engine (SQLite, PostgreSQL, MySQL …) | `SQLite` |
| `<DB_PATH>` | Connection string / path used by every storage class | `storage/database/<PROJECT>.db` |
| `<DDL_SCRIPT>` | The one file holding the full schema | `storage/SQL_Scripts/create-schema.sql` |
| `<UI_LANGUAGE>` | Language of all user-facing text | |
| `<CSS_FRAMEWORK>` | CSS framework + exact version, loaded from CDN | `Bootstrap 5.3.x` |
| `<MAIN_BRANCH>` | Long-lived branch | `main` |
| `<Entity>` / `<entity>` | A single domain object, PascalCase / snake_case | e.g. `Invoice` / `invoice` |
| `<Entities>` / `<entities>` | Plural of the above | e.g. `Invoices` / `invoices` |

**The worked example** used throughout this document is a `Customer` entity in a generic sales
domain. Replace `Customer` / `customer` / `customers` / `Customers` with your own entity when you
use the recipe in §12.

### Reference implementation

Nominate **one feature** in your project as the reference implementation — the one new code is
copied from. Name it here, and keep it clean:

> Reference feature: `<entity>` — `models/<entity>.py` → `storage/db_<entities>.py` →
> `services/<entity>_service.py` → routes in `app.py` → `templates/<entities>/`

---

## 1. Architecture — three layers

A classic 3-layer architecture. Each layer only talks to the layer directly below it, and
**never skips a layer**.

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
  Data access       storage/db_*.py                    (CRUD against <DB_ENGINE>)
     |
     v
  Database          <DB_PATH>

  Shared:           models/*.py                        (plain data classes, used by all layers)
```

Why: responsibility is separated, each part is manageable on its own, the code is easier to change
and maintain, and logic can be reused.

### The rules that keep the layers apart

| Rule | Why |
| --- | --- |
| `app.py` never imports the database driver and never imports from `storage/` | Routes must not know how data is stored |
| `services/` never imports `flask`, never touches `request` or `render_template` | Business logic must be testable without a web server |
| `storage/` never imports from `services/` | Data access is the bottom layer; it only knows models |
| `models/` imports nothing from the other layers | Models are the shared vocabulary |
| Templates only read from objects handed to them by the route | No logic in the view beyond loops, `if` and formatting |

**Accepted exception:** a model may import another model. Inheritance or composition between domain
objects is a modelling decision, not a layering violation.

**How to check the rules quickly:**

```bash
grep -rn "import sqlite3\|from storage" app.py                  # must return nothing
grep -rn "flask\|request\|render_template" services/ storage/   # must return nothing
grep -rn "from services" storage/                               # must return nothing
```

### Where does this piece of code belong?

| The code … | Layer |
| --- | --- |
| reads `request.form`, calls `render_template`, redirects | Presentation (`app.py`) |
| decides a rule, calculates, validates, coordinates two entities | Business logic (`services/`) |
| writes SQL, opens a connection, maps a row to an object | Data access (`storage/`) |
| just holds field values | Model (`models/`) |

If a piece of code seems to belong in two layers, it is two pieces of code.

---

## 2. Folder and file naming

```
<PROJECT_NAME>/
├── app.py                  all Flask routes
├── README.md
├── .gitignore
├── docs/
│   └── CODESTANDARD.md     this file
├── models/                 plain data classes
├── services/               business logic
├── storage/
│   ├── db_*.py             data access
│   ├── database/           the database file (gitignored)
│   └── SQL_Scripts/        <DDL_SCRIPT> — the schema, committed
├── static/
│   └── style.css
├── templates/
│   ├── layout.html         the one layout every page extends
│   └── <entities>/         one folder per feature
└── tests/
    └── test_<entity>.py
```

| Folder | File name pattern | Example |
| --- | --- | --- |
| `models/` | `<singular_noun>.py` | `customer.py`, `invoice_line.py` |
| `services/` | `<singular_noun>_service.py` | `customer_service.py` |
| `storage/` | `db_<plural_noun>.py` | `db_customers.py` |
| `templates/` | `<plural_noun>/<page>.html` | `customers/create-customer.html` |
| `tests/` | `test_<model>.py` | `test_customer.py` |

- Python files: `snake_case`.
- HTML template files: `kebab-case` (`create-customer.html`, `edit-invoice.html`).
- The list page is named after its folder: `customers/customers.html`.

---

## 3. Naming inside the code

| Element | Convention | Example |
| --- | --- | --- |
| Model class | `PascalCase`, singular | `Customer`, `InvoiceLine` |
| Service class | `PascalCase` + `Service` | `CustomerService` |
| Storage class | `Storage_<Singular>` | `Storage_Customer` |
| Method / function | `snake_case` | `get_customer_by_id` |
| Private field | `self.__name` (double underscore) | `self.__storage` |
| Private method | `__name` | `__create_table_if_missing` |
| SQL constant | `UPPER_SNAKE_CASE` ending in `_SQL` | `SELECT_BY_ID_SQL` |
| Database table | `PascalCase`, plural | `Customers`, `InvoiceLines` |
| Database column | `PascalCase` | `CustomerId`, `CreditLimit` |
| Route function | `snake_case`, matches the action | `create_customer` |
| Form field name | `snake_case`, matches the model property | `name`, `credit_limit` |

**The deliberate mismatch:** Python is `snake_case`, SQL is `PascalCase`. Do not rename columns to
match Python — the mapping happens in the storage layer and nowhere else.

Pick a convention for each row above once, write it down here, and never mix two styles in the same
project. A consistent wrong convention costs less than an inconsistent right one.

---

## 4. Models

A model is a **plain class with private fields exposed through `@property`**. It is the shared
vocabulary of the application: routes, services, storage and templates all speak in models.

```python
class Customer:
    def __init__(self, id, name, email, city, credit_limit):
        self.__id = id
        self.__name = name
        self.__email = email
        self.__city = city
        self.__credit_limit = credit_limit

    @property
    def id(self):
        return self.__id            # id has NO setter — it is assigned by the database

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        self.__name = new_name

    # … one getter + one setter per remaining field
```

Rules:

1. All fields are private (`self.__field`).
2. Every field gets a `@property` getter.
3. Every field gets a setter **except `id`**, and except foreign keys or values that must not change
   after creation.
4. The setter parameter is named `new_<field>`.
5. The constructor parameter order **must match the column order of the table**, because storage
   builds models with `Model(*row)`. Getting this wrong silently shifts every value — the app will
   run and show nonsense.
6. No database code, no Flask code, no validation logic in a model.
7. Add `to_json()` only if the model is exposed through a JSON API:

```python
    def to_json(self):
        return {
            "id": self.__id,
            "name": self.__name,
            "email": self.__email,
        }
```

---

## 5. Data access (storage)

One class per table group, constructed with **no arguments**, opening its own connection.

```python
import sqlite3
from models.customer import Customer


class Storage_Customer:
    SELECT_ALL_SQL   = "SELECT * FROM Customers"
    SELECT_BY_ID_SQL = SELECT_ALL_SQL + " WHERE Id = (?)"
    INSERT_SQL       = "INSERT INTO Customers(Name, Email, City, CreditLimit) VALUES(?, ?, ?, ?)"
    UPDATE_SQL       = "UPDATE Customers SET Name = (?), Email = (?), City = (?), CreditLimit = (?) WHERE Id = (?)"
    DELETE_SQL       = "DELETE FROM Customers WHERE Id = (?)"

    def __init__(self):
        self.__connection = sqlite3.connect("<DB_PATH>", check_same_thread=False)
        self.__create_table_if_missing()

    def __create_table_if_missing(self):
        cur = self.__connection.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS Customers(
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name VARCHAR(100),
                Email VARCHAR(100),
                City VARCHAR(50),
                CreditLimit INTEGER
            )
            """
        )
        self.__connection.commit()
        cur.close()

    def get_all_customers(self):
        cur = self.__connection.cursor()
        cur.execute(self.SELECT_ALL_SQL)
        customers = []
        for row in cur:
            customers.append(Customer(*row))
        cur.close()
        return customers

    def get_customer_by_id(self, id):
        cur = self.__connection.cursor()
        cur.execute(self.SELECT_BY_ID_SQL, (id,))
        row = cur.fetchone()
        cur.close()
        if row is None:
            return None
        return Customer(*row)

    def add_customer(self, customer: Customer):
        cur = self.__connection.cursor()
        cur.execute(self.INSERT_SQL,
                    (customer.name, customer.email, customer.city, customer.credit_limit))
        self.__connection.commit()
        return cur.lastrowid

    def update_customer(self, customer: Customer):
        cur = self.__connection.cursor()
        cur.execute(self.UPDATE_SQL,
                    (customer.name, customer.email, customer.city, customer.credit_limit, customer.id))
        self.__connection.commit()
        cur.close()

    def delete_customer(self, id):
        cur = self.__connection.cursor()
        cur.execute(self.DELETE_SQL, (id,))
        self.__connection.commit()
        cur.close()
```

Rules:

1. **Always parameterised SQL** — `(?)` placeholders and a tuple of values. Never build SQL by
   concatenating or interpolating values, not even "safe" ones. No f-strings on SQL constants; an
   f-prefix on a constant string does nothing today and invites a real injection tomorrow.
2. SQL lives in `UPPER_SNAKE_CASE` class constants at the top of the class, never inline in a method.
3. The connection string is the literal `<DB_PATH>`, identical in every storage class.
   `check_same_thread=False` is required for SQLite because the Flask dev server serves requests on
   several threads.
4. Rows become models with `Model(*row)` — which is why §4 rule 5 exists.
5. `add_*` returns the generated id (`cur.lastrowid`) so the service can learn it.
6. `commit()` after every INSERT / UPDATE / DELETE.
7. `cur.close()` when the cursor is finished with.
8. `SELECT` by id uses `fetchone()` and returns `None` when there is no row. Never let a loop
   variable leak out of an empty `for row in cur:` — that raises `UnboundLocalError` on a miss.
9. Tables are created defensively with `CREATE TABLE IF NOT EXISTS` in a private
   `__create_table_if_missing()` called from `__init__`. **The same DDL also goes into
   `<DDL_SCRIPT>`**, so a fresh database can be built from the script. Both are required — the
   database file is gitignored, so the script is the only record of the schema in the repository.
10. Storage does **no business logic** — no sorting rules, no defaults, no validation.

### The standard method set

Every storage class exposes the same shape, so a reader knows what to expect:

```
get_all_<plural>()          -> list[Model]
get_<singular>_by_id(id)    -> Model | None
get_<plural>_by_<fk>(fk)    -> list[Model]     (optional)
add_<singular>(model)       -> int (new id)
update_<singular>(model)    -> None
delete_<singular>(id)       -> None
```

---

## 6. Business logic (services)

```python
from models.customer import Customer
from storage.db_customers import Storage_Customer


class CustomerService:
    def __init__(self):
        self.__storage = Storage_Customer()

    def get_all_customers(self):
        """
        Getting all customers from storage
        """
        return self.__storage.get_all_customers()

    def get_customer_by_id(self, id):
        """
        Getting customer by id from storage
        """
        return self.__storage.get_customer_by_id(id)

    def create_customer(self, name, email, city, credit_limit):
        """
        Creating customer and adding to storage
        """
        customer = Customer(None, name, email, city, credit_limit)
        created_id = self.__storage.add_customer(customer)
        return Customer(created_id, name, email, city, credit_limit)

    def update_customer(self, id, name, email, city, credit_limit):
        """
        Updating customer in storage
        """
        customer = Customer(id, name, email, city, credit_limit)
        self.__storage.update_customer(customer)
        return customer

    def delete_customer(self, id):
        """
        Deleting customer from storage
        """
        self.__storage.delete_customer(id)
```

Rules:

1. The service **owns** its storage object in `self.__storage` — created in `__init__`, never
   passed in.
2. Services take and return **models and primitives** — never database rows, never `request.form`,
   never a Flask object.
3. `create_*` builds the model with `id = None`, calls `add_*`, and returns a model carrying the
   new id.
4. Every public method has a short `"""docstring"""` in one consistent style. This project uses the
   present participle: *"Getting all customers from storage"*, *"Creating invoice and adding to
   storage"*.
5. **Cross-entity work happens by passing the other service in as an argument, not by importing it.**
   This is the rule that keeps the service layer free of circular imports:

```python
    def create_invoice(self, customer_id, amount, customer_service):
        """
        Creating invoice for an existing customer
        """
        customer = customer_service.get_customer_by_id(customer_id)
        if customer is None:
            return None
        ...
```

6. Return type hints where the return is a list of models:
   `def get_open_invoices(self) -> list[Invoice]:`.
7. `create_some_<entities>()` seed helpers are a project convention for demo data — one method that
   inserts a handful of realistic rows, reachable from a route so the app is quick to try out.

### This is where the rules live

Anything that is not "read or write a row" belongs here — not in the route, not in storage.
Typical examples in any domain:

- a uniqueness or exclusivity rule ("only one primary contact per customer");
- a range or date rule ("the due date may not be before the invoice date");
- a cascade ("deleting a customer also deletes their invoices");
- a calculation ("order total is the sum of the lines plus VAT");
- a sort order that means something in the domain ("rank by points, then by margin").

If you cannot decide whether something is a rule: if it could ever change because the *business*
changed its mind, it is a rule and it goes in a service.

---

## 7. Presentation — routes

All routes live in the single file `app.py`. Services are instantiated **once at module level**:

```python
from flask import Flask, render_template, request, redirect, url_for
from services.customer_service import CustomerService
from services.invoice_service import InvoiceService

app = Flask(__name__)

customer_service = CustomerService()
invoice_service = InvoiceService()
```

### Route layout

Sections are separated by a full-width comment banner, one per feature:

```python
#------------------------------------------------------------------------------------------------------------------------------
# Customer administration
#------------------------------------------------------------------------------------------------------------------------------
```

Keep related features next to each other, in the order they appear in the navigation bar.

### URL patterns

| Action | URL | Methods |
| --- | --- | --- |
| List | `/<entities>` | GET |
| Create | `/<entities>/create` | GET, POST |
| Edit | `/<entities>/<int:id>/edit` | GET, POST |
| Delete | `/<entities>/<int:id>/delete` | GET |
| Sub-action | `/<entities>/<int:id>/<verb>` | GET or POST |
| JSON | `/api/<entities>` | GET |

### Handler shape

Create and edit are **each one function** with a `request.method` branch:

```python
@app.route('/customers/<int:id>/edit', methods=['GET', 'POST'])
def edit_customer(id):
    if request.method == "POST":
        customer_service.update_customer(
            id,
            request.form['name'],
            request.form['email'],
            request.form['city'],
            int(request.form['credit_limit'])
        )
        return redirect(url_for("customers"))
    else:
        return render_template('customers/edit-customer.html', title = 'Edit customer',
                               customer = customer_service.get_customer_by_id(id))
```

Rules:

1. A POST always ends in `redirect(url_for(...))` — never render a template after a POST.
   (Post/Redirect/Get, so refreshing the browser does not re-submit the form.)
2. Use `url_for("<route function name>")`, not a hard-coded path.
3. **Type conversion happens in the route**: `int(request.form['credit_limit'])`. The service
   receives correct types and never has to parse strings.
4. Every `render_template` passes `title = '…'` in `<UI_LANGUAGE>`; the layout renders it both in
   `<title>` and as the page `<h2>`.
5. Keyword arguments to `render_template` are named exactly as the template expects them.
6. Routes contain **no database loops and no calculations**. The one accepted exception is a small
   view-model dictionary assembled purely to make the template simpler (a lookup dict, a count per
   id) — and even then, prefer a service method.
7. Docstrings on non-obvious routes only. A four-line CRUD route documents itself.
8. Delete is a plain GET link guarded by a JavaScript `confirm()` in the template.
9. A route may use several services (for example, to fill a dropdown). It may not use any storage
   class.

---

## 8. Presentation — templates

Every page extends the single layout:

```jinja
{% extends 'layout.html' %}
{% block content %}
    ...
{% endblock %}
```

`templates/layout.html` holds `<head>`, the `<CSS_FRAMEWORK>` CDN link, `/static/style.css`, the
navigation bar, and the `title` → `<h2>` block:

```html
<!DOCTYPE html>
<html>
    <head>
        {% if title %}<title>{{title}}</title>{% else %}<title>Missing title</title>{% endif %}
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css">
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <a class="navbar-brand" href="/">Home</a>
            <div class="navbar-nav">
                <a class="nav-item nav-link" href="/customers">Customer administration</a>
                <!-- one entry per top-level feature -->
            </div>
        </nav>
        <div class="container">
            <h2>{{title}}</h2>
            {% block content %}{% endblock %}
        </div>
    </body>
</html>
```

Rules:

1. New top-level features get one `nav-item nav-link` entry in `layout.html`.
2. Styling is `<CSS_FRAMEWORK>` classes (`table`, `form-control`, `btn btn-outline-primary`,
   `col-4`). `static/style.css` is only for the few things the framework does not cover.
   No inline `style=` attributes.
3. **All user-facing text is `<UI_LANGUAGE>`. Code, comments, docstrings and identifiers are always
   English.** Do not mix the two inside one file.
4. On list pages, the **Id cell is the link to the edit page**:
   `<td><a href='/customers/{{customer.id}}/edit'>{{customer.id}}</a></td>`.
5. Forms: `<form action="#" method="post">` inside `<div class="col-4">`, inputs wrapped in
   `<div class="form-group">`, with `<label for="x">`, `name="x"` and `id="x"` **all matching the
   `request.form['x']` key used in the route**, which in turn matches the model property.
6. Create forms pre-fill sensible demo values (`value="Acme A/S"`, `value="2026"`) so the app is
   quick to try out. Edit forms fill from the model (`value="{{customer.name}}"`), with the `id`
   field `readonly`.
7. Delete uses this confirm-script pattern, placed in the edit template:

```html
<input type="button" class="btn btn-outline-danger form-control" value="Delete"
       onclick="return confirmdelete({{customer.id}})">
<script>
    function confirmdelete(customerid) {
        deleteconfirmed = confirm('Are you sure you want to delete this customer?');
        if (deleteconfirmed == true) {
            window.location.href = '/customers/' + customerid + '/delete';
        } else {
            return false;
        }
    }
</script>
```

8. Loop variables are spelled out, not abbreviated: `{% for customer in customers %}`, not
   `{% for c in customers %}`.

---

## 9. Tests

Tests use the standard-library `unittest`, **one file per model**.

```python
import unittest

from models.customer import Customer


class TestCustomerModel(unittest.TestCase):
    def test_initial_values(self):
        customer = Customer(id=10, name='Acme A/S', email='post@acme.example',
                            city='Aarhus', credit_limit=50000)

        self.assertEqual(customer.id, 10)
        self.assertEqual(customer.name, 'Acme A/S')
        self.assertEqual(customer.email, 'post@acme.example')
        self.assertEqual(customer.city, 'Aarhus')
        self.assertEqual(customer.credit_limit, 50000)

    def test_name_setter_updates_value(self):
        customer = Customer(id=1, name='Acme A/S', email='post@acme.example',
                            city='Aarhus', credit_limit=50000)

        customer.name = 'Acme Holding A/S'
        self.assertEqual(customer.name, 'Acme Holding A/S')


if __name__ == "__main__":
    unittest.main()
```

Rules:

1. Class name `Test<Model>Model`; method names `test_<what>_<expected>`.
2. The constructor is called with **keyword arguments** — this is what makes the test double as a
   check that parameter names have not drifted from the table columns.
3. One `test_initial_values` covering the constructor, then one test per setter.
4. Models are tested in isolation — no database, no Flask, no mocks needed. That is the payoff for
   keeping models plain.
5. Run from the project root so the packages resolve:

```
python -m unittest discover -s tests -t .
```

6. A service method that contains a **real rule** (not a pass-through to storage) is worth a test
   too. Be aware that a service opens a real database connection in `__init__`, so such a test
   touches the real database file — keep those tests read-only, or point `<DB_PATH>` at a temporary
   file first.

**When a test fails, fix the code or fix the test — never delete the test.** A test file that
cannot pass is worse than no test, because it makes the whole suite untrustworthy.

---

## 10. Git and branching

- Branch off `<MAIN_BRANCH>`, **one branch per feature**, named after the feature
  (`customer-administration`, `invoice-pdf-export`).
- Commit messages are short and describe the feature, in English:
  `add unit test customer for model`, `customer administration added`.
- Open a pull request against `<MAIN_BRANCH>`; use the checklist in §12 as the PR description.

### What must never be committed

`.gitignore` excludes at minimum:

```
__pycache__/
*.pyc
storage/database/*.db
.env
```

**The database file is never committed.** The consequence is a hard rule:

> A schema change must go into **both** `<DDL_SCRIPT>` **and** the `CREATE TABLE IF NOT EXISTS` in
> the storage class — otherwise the feature will not work on another machine.

Secrets (API keys, connection passwords) are never committed either. They are read from environment
variables:

```python
import os
API_KEY = os.environ.get("<PROJECT>_API_KEY")
```

---

## 11. Known deviations — do not copy these

Keep a table here of code that exists but is **not** the standard. This section is what keeps the
document honest: it is the difference between "the standard" and "whatever happens to be in the
repo".

| File | Issue | Fix when you touch it |
| --- | --- | --- |
| _(example)_ `storage/db_x.py` | Class copy-pasted from another file, still carries the wrong name | Rename to `Storage_X` |
| _(example)_ `tests/test_y.py` | Constructor arguments do not match the model — the test cannot pass | Update the test to the real signature |
| | | |

Rules for this table:

- Every row names a real file and a concrete problem.
- Fix the row when you next edit that file, then delete the row.
- If the table is empty, say so explicitly. An empty table means "the code matches the standard".

---

## 12. Recipe — how to add a new feature

A step-by-step recipe for adding a new CRUD feature. The worked example is a **`Customer`** feature.
Replace `Customer` / `customer` / `customers` / `Customers` throughout with your own entity.

### Step 0 — Before you start

```
git checkout <MAIN_BRANCH>
git pull
git checkout -b customer-administration
```

Check that the app runs and the database exists:

```
python app.py
```

The database file is not in git. If you do not have it, create it from `<DDL_SCRIPT>`.

### The order of work

Build **bottom-up**. Each step runs and can be checked before you move on.

```
  1. Database table        <DDL_SCRIPT> + CREATE TABLE IF NOT EXISTS
  2. Model                 models/customer.py
  3. Storage               storage/db_customers.py
  4. Service               services/customer_service.py
  5. Routes                app.py
  6. Templates             templates/customers/*.html
  7. Navigation            templates/layout.html
  8. Test                  tests/test_customer.py
  9. Run it, then commit
```

**Do not start with the HTML.** The template is the last thing that can be written, because it
depends on names decided in every layer below it.

---

### Step 1 — Database table

Decide the columns first. **The column order fixes the constructor order of the model**, because
storage builds models with `Model(*row)`.

| Column | Type | Note |
| --- | --- | --- |
| `Id` | INTEGER PRIMARY KEY AUTOINCREMENT | always first |
| `Name` | VARCHAR(100) | |
| `Email` | VARCHAR(100) | |
| `City` | VARCHAR(50) | |
| `CreditLimit` | INTEGER | |

Append the table to `<DDL_SCRIPT>`:

```sql
CREATE TABLE Customers(
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Name VARCHAR(100),
    Email VARCHAR(100),
    City VARCHAR(50),
    CreditLimit INTEGER
);
```

A foreign key spells out the referenced table:

```sql
    CustomerId INTEGER NOT NULL,
    FOREIGN KEY (CustomerId) REFERENCES Customers(Id)
```

You will add the same table again as `CREATE TABLE IF NOT EXISTS` in step 3. Both are required.

---

### Step 2 — Model

Create `models/customer.py` following §4: private fields, a getter for everything, a setter for
everything except `id`, constructor order matching the table.

Checklist:

- [ ] Class `Customer`, file `models/customer.py`.
- [ ] Constructor parameter order == column order in step 1.
- [ ] `id` has a getter and **no** setter.
- [ ] Setter parameters named `new_<field>`.
- [ ] No imports except other models.

---

### Step 3 — Storage

Create `storage/db_customers.py` by copying the reference implementation named in §0, and following §5.

Checklist:

- [ ] Class named `Storage_Customer`.
- [ ] All SQL in `_SQL` constants; all values passed as `(?)` parameters — never string-formatted in.
- [ ] `Id` is **not** in the `INSERT` column list; the database generates it.
- [ ] `add_customer` returns `cur.lastrowid`.
- [ ] `get_customer_by_id` returns `None` when there is no row.
- [ ] `commit()` after insert/update/delete, `cur.close()` when done.
- [ ] `CREATE TABLE IF NOT EXISTS` matches the DDL from step 1, column for column.
- [ ] Nothing here decides business rules.

---

### Step 4 — Service

Create `services/customer_service.py` following §6.

Checklist:

- [ ] Class `CustomerService`, owns `self.__storage = Storage_Customer()`.
- [ ] `get_all_`, `get_..._by_id`, `create_`, `update_`, `delete_`.
- [ ] A docstring on every public method, in the project's docstring style.
- [ ] No `flask` import, no SQL.
- [ ] Every rule from the domain lives here — and only here.
- [ ] Anything needing another entity takes that service as a **parameter**.

---

### Step 5 — Routes

In `app.py`:

**5a.** Import and instantiate the service at the top, next to the others:

```python
from services.customer_service import CustomerService
...
customer_service = CustomerService()
```

**5b.** Add a section banner and the four routes, placed next to related features:

```python
#------------------------------------------------------------------------------------------------------------------------------
# Customer administration
#------------------------------------------------------------------------------------------------------------------------------
@app.route('/customers')
def customers():
    return render_template('customers/customers.html', title = 'Customers',
                           customers = customer_service.get_all_customers())

@app.route('/customers/create', methods=['GET', 'POST'])
def create_customer():
    if request.method == "POST":
        customer_service.create_customer(
            request.form['name'],
            request.form['email'],
            request.form['city'],
            int(request.form['credit_limit'])
        )
        return redirect(url_for("customers"))
    else:
        return render_template('customers/create-customer.html', title = 'Create customer')

@app.route('/customers/<int:id>/edit', methods=['GET', 'POST'])
def edit_customer(id):
    if request.method == "POST":
        customer_service.update_customer(
            id,
            request.form['name'],
            request.form['email'],
            request.form['city'],
            int(request.form['credit_limit'])
        )
        return redirect(url_for("customers"))
    else:
        return render_template('customers/edit-customer.html', title = 'Edit customer',
                               customer = customer_service.get_customer_by_id(id))

@app.route('/customers/<int:id>/delete')
def delete_customer(id):
    customer_service.delete_customer(id)
    return redirect(url_for("customers"))
```

Checklist:

- [ ] URLs are `/customers`, `/customers/create`, `/customers/<int:id>/edit`, `/customers/<int:id>/delete`.
- [ ] Create and edit are one function each with an `if request.method == "POST":` branch.
- [ ] Every POST branch ends in `redirect(url_for(...))` — never a `render_template`.
- [ ] Numbers converted with `int(...)` **in the route**.
- [ ] Every `render_template` passes a `<UI_LANGUAGE>` `title`.
- [ ] Dropdown data comes from another service — a route may use several services.
- [ ] No database driver, no SQL, no rules in `app.py`.

---

### Step 6 — Templates

Create `templates/customers/` with three files.

**6a. `customers.html` — the list**

```jinja
{% extends 'layout.html' %}
{% block content %}
    <p>&nbsp;</p>
    <table class="table">
    <thead>
        <tr>
            <th>Id</th><th>Name</th><th>Email</th><th>City</th><th>Credit limit</th>
        </tr>
    </thead>
    <tbody>
    {% for customer in customers %}
        <tr>
            <td><a href='/customers/{{customer.id}}/edit'>{{customer.id}}</a></td>
            <td>{{customer.name}}</td>
            <td>{{customer.email}}</td>
            <td>{{customer.city}}</td>
            <td>{{customer.credit_limit}}</td>
        </tr>
    {% endfor %}
    </tbody>
    </table>
    <p>&nbsp;</p>
    Create a new customer — <a href="/customers/create">create customer</a>
{% endblock %}
```

**6b. `create-customer.html`**

```jinja
{% extends 'layout.html' %}
{% block content %}
    <div class="col-4">
        <form action="#" method="post">
            <div class="form-group">
                <label for="name">Name:</label>
                <input type="text" name="name" id="name" class="form-control" value="Acme A/S" required>

                <label for="email">Email:</label>
                <input type="email" name="email" id="email" class="form-control" value="post@acme.example" required>

                <label for="city">City:</label>
                <input type="text" name="city" id="city" class="form-control" value="Aarhus" required>

                <label for="credit_limit">Credit limit:</label>
                <input type="number" name="credit_limit" id="credit_limit" class="form-control" value="50000" required>

                <br>
                <input type="submit" class="form-control" value="Create customer">
            </div>
        </form>
    </div>
{% endblock %}
```

A foreign key is a `<select>` filled from the other service:

```jinja
                <label for="customerid">Customer:</label>
                <select name="customerid" id="customerid" class="form-control" required>
                    {% for customer in customers %}
                        <option value="{{customer.id}}">{{customer.name}}</option>
                    {% endfor %}
                </select>
```

**6c. `edit-customer.html`** — the same form, with `id` readonly, values taken from the model, an
Update submit, and the delete confirm script from §8 rule 7. On an edit form, a `<select>` marks
the current value:

```jinja
<option value="{{customer.id}}" {% if customer.id == invoice.customerid %}selected{% endif %}>{{customer.name}}</option>
```

Checklist:

- [ ] Each file starts with `{% extends 'layout.html' %}` and wraps everything in `{% block content %}`.
- [ ] Every `name="x"` matches a `request.form['x']` in the route, and matches the model property.
- [ ] All visible text is `<UI_LANGUAGE>`.
- [ ] `<CSS_FRAMEWORK>` classes only; no inline `style=`.
- [ ] The Id column on the list page links to the edit page.
- [ ] Delete goes through the `confirmdelete` script.

---

### Step 7 — Navigation

Add the entry to the navbar in `templates/layout.html`, in the same order as the app flow:

```html
<a class="nav-item nav-link" href="/customers">Customer administration</a>
```

---

### Step 8 — Test

Create `tests/test_customer.py` following §9: one test for the constructor, one per setter,
constructed with keyword arguments. Run from the project root:

```
python -m unittest discover -s tests -t .
```

---

### Step 9 — Run it and commit

```
python app.py
```

Click through the whole flow in the browser:

1. `/customers` — the list renders (empty is fine).
2. `/customers/create` — any dropdown is populated; submit redirects back to the list.
3. Click an Id — the edit form is pre-filled, and the correct dropdown value is selected.
4. Change a value, press *Update* — the change shows in the list.
5. Press *Delete* — the confirm dialog appears, and the row disappears.
6. The navbar link works from every page.

```
git add .
git commit -m "customer administration added"
git push -u origin customer-administration
```

Then open a pull request against `<MAIN_BRANCH>`.

---

### Quick checklist — copy into your pull request

```
- [ ] Table added to <DDL_SCRIPT>
- [ ] CREATE TABLE IF NOT EXISTS in the storage class __init__ (identical DDL)
- [ ] models/<entity>.py           private fields, properties, no setter on id, ctor order = column order
- [ ] storage/db_<entities>.py     Storage_<Entity>, _SQL constants, parameterised queries, commit + close
- [ ] services/<entity>_service.py owns its storage, docstrings, all rules live here
- [ ] app.py                       service instantiated at module level, 4 routes, POST -> redirect
- [ ] templates/<entities>/        list + create + edit, extends layout.html, <UI_LANGUAGE> text
- [ ] layout.html                  navbar entry
- [ ] tests/test_<entity>.py       constructor + one test per setter, all tests pass
- [ ] Clicked through create / edit / delete in the browser
- [ ] No DB driver or SQL in app.py; no flask import in services/ or storage/
- [ ] No secrets and no .db file in the commit
```

---

## 13. Variations on the recipe

### A feature that only reads data (no table of its own)

A report, a dashboard, an aggregated view. No storage class at all: the service composes data from
other services passed in as arguments, and the route just renders the result.

```python
class ReportService:
    def get_customer_overview(self, customer_service, invoice_service) -> list[dict]:
        """
        Building the customer overview from customers and invoices
        """
        ...
```

### A feature spanning several tables

One storage class owns all the closely related tables — the ones created together, written together,
and never used apart — with **one model per table**, and one service holding the logic that spans
them. Example shape: `Order`, `OrderLine`, `OrderStatusHistory` → `storage/db_orders.py` →
`services/order_service.py`.

### A feature that reads an external API

The code that calls the API is still a service — the route must not call it directly, and no other
layer imports the HTTP client. The API key comes from an environment variable (§10), never from a
literal in the source. Map the API response into your own models immediately, so the rest of the app
never sees the foreign shape.

### A JSON endpoint

Give the model a `to_json()` method (§4 rule 7), add a service method returning a list of those
dictionaries, and return it directly from the route:

```python
@app.route('/api/customers', methods = ['GET'])
def get_all_customers_json():
    """
    Exposing customers as JSON
    """
    return customer_service.get_all_customers_json()
```

### A sub-action on an existing entity

Anything that is not plain CRUD — "generate schedule", "send reminder", "close order" — is a
sub-action route `/<entities>/<int:id>/<verb>` that calls one service method and redirects back to
where the user was. The verb's logic lives entirely in the service.

---

## 14. Adapting this template to a new project

1. Copy this file to `docs/CODESTANDARD.md` in the new repository.
2. Fill in [§0](#0-project-variables). Do a find-and-replace on every `<PLACEHOLDER>`.
3. Delete the quote block at the top of the file.
4. Decide your entities. Write them down: for each one, the table name, its columns in order, and
   its relationships. That list *is* the plan for the whole application.
5. Build the **first** entity end-to-end with the §12 recipe. Do not start the second until the
   first works in the browser. Nominate it as the reference implementation in §0.
6. Rewrite the examples in §§4–9 to use that real entity, so this document points at real files in
   *your* repository rather than at `Customer`.
7. Keep §11 (known deviations) current. It is what stops the document from drifting into fiction.

### What to change per project, and what to keep

| Safe to change | Keep |
| --- | --- |
| Entity, table and route names | The three layers, and the rules that keep them apart |
| `<UI_LANGUAGE>`, `<CSS_FRAMEWORK>`, `<DB_ENGINE>` | Models as plain classes with properties |
| The number of features | One storage class per table group; parameterised SQL only |
| Splitting `app.py` into Flask blueprints once it passes a few hundred lines | The standard method set and the CRUD URL pattern |
| Swapping `unittest` for `pytest` | Post/Redirect/Get, and type conversion in the route |
| Adding a migrations tool instead of `CREATE TABLE IF NOT EXISTS` | Schema committed to the repo; database file never committed |

The point of the structure is not the specific names. It is that **a developer who has read one
feature can predict where every line of the next feature lives.** Any change that preserves that is
in the spirit of this document; any change that breaks it is not.
