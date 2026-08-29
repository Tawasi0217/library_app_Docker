# Library Loan Flask App

Flask + Flask-SQLAlchemy library loan management app.

## Miniconda Setup

```powershell
conda env create -f environment.yml
conda activate library-loan-app
python init_db.py
python app.py
```

`python init_db.py` creates SQLite tables and inserts seed data.
The SQLite file is created as `library.db` under Flask's instance path.

## Main Pages

- `http://127.0.0.1:5000/books`: book list and genre filter
- `http://127.0.0.1:5000/books/new`: create book
- `http://127.0.0.1:5000/users`: user list and keyword filter
- `http://127.0.0.1:5000/users/new`: create user
- `http://127.0.0.1:5000/borrows`: active borrow list and return action
- `http://127.0.0.1:5000/borrows/new`: create borrow
- `http://127.0.0.1:5000/auth/login`: login
- `http://127.0.0.1:5000/auth/signup`: signup

## Checklist Support

- Template engine: all pages are rendered with Jinja templates under `templates/`.
- WTForms: create/edit/delete/auth/borrow forms are defined in `forms.py`.
- Validators: built-in validators and custom validators are defined in `validators.py`.
- Filter feature: book genre filtering and user keyword filtering are implemented.
- Custom Jinja filters: `datetime_jp` and `stock_status` are registered in `app.py`.
- Error handling: 404 and 500 handlers render templates under `templates/errors/`.
- Flask `g`: `g.admin_user` is loaded in `app.py` and shown in `templates/base.html`.

Blueprints can import shared objects like this:

```python
from extensions import db
from models import AdminUser, Book, Borrow, User
```
