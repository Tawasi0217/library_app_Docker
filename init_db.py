import os

from werkzeug.security import generate_password_hash

from app import create_app
from extensions import db
from models import AdminUser, Book, User


BOOK_SEEDS = [
    {"title": "Clean Code", "author": "Robert C. Martin", "genre": "Programming", "stock": 3},
    {"title": "The Pragmatic Programmer", "author": "Andrew Hunt, David Thomas", "genre": "Programming", "stock": 2},
]
USER_SEEDS = [
    {"name": "Taro Yamada", "email": "taro@example.com"},
    {"name": "Hanako Sato", "email": "hanako@example.com"},
]


def seed_data():
    # Demo accounts and books are opt-in, never added to production implicitly.
    if os.getenv("SEED_DEMO_DATA", "").lower() in ("1", "true", "yes"):
        for data in USER_SEEDS:
            if not User.query.filter_by(email=data["email"]).first():
                db.session.add(User(**data))
        for data in BOOK_SEEDS:
            if not Book.query.filter_by(title=data["title"]).first():
                db.session.add(Book(**data))

    username = os.environ.get("ADMIN_USERNAME", "admin")
    password = os.environ.get("ADMIN_PASSWORD")
    if password and len(password) < 8:
        raise ValueError("ADMIN_PASSWORD must contain at least 8 characters")
    if password and not AdminUser.query.filter_by(username=username).first():
        db.session.add(AdminUser(
            username=username, password_hash=generate_password_hash(password)
        ))
    db.session.commit()


def init_db():
    app = create_app()
    with app.app_context():
        db.create_all()
        seed_data()


if __name__ == "__main__":
    init_db()
    print("Database initialized.")
