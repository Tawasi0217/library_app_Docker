from app import create_app
from extensions import db
from models import AdminUser, Book, User
from werkzeug.security import generate_password_hash


BOOK_SEEDS = [
    {
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "genre": "Programming",
        "stock": 3,
    },
    {
        "title": "The Pragmatic Programmer",
        "author": "Andrew Hunt, David Thomas",
        "genre": "Programming",
        "stock": 2,
    },
]

USER_SEEDS = [
    {"name": "Taro Yamada", "email": "taro@example.com"},
    {"name": "Hanako Sato", "email": "hanako@example.com"},
]

ADMIN_SEED = {
    "username": "admin",
    "password": "admin-password",
}


def seed_data():
    for user_data in USER_SEEDS:
        user = User.query.filter_by(email=user_data["email"]).first()
        if user is None:
            db.session.add(User(**user_data))

    for book_data in BOOK_SEEDS:
        book = Book.query.filter_by(title=book_data["title"]).first()
        if book is None:
            db.session.add(Book(**book_data))

    admin = AdminUser.query.filter_by(username=ADMIN_SEED["username"]).first()
    if admin is None:
        db.session.add(
            AdminUser(
                username=ADMIN_SEED["username"],
                password_hash=generate_password_hash(ADMIN_SEED["password"]),
            )
        )

    db.session.commit()


def init_db():
    app = create_app()
    with app.app_context():
        db.create_all()
        seed_data()


if __name__ == "__main__":
    init_db()
    print("Database initialized and seed data inserted.")
