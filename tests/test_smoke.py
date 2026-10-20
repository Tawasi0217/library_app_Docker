import pytest
from app import create_app
from extensions import db
from models import AdminUser, Book
from werkzeug.security import generate_password_hash


@pytest.fixture()
def client(tmp_path):
    app = create_app({
        "TESTING": True,
        "SECRET_KEY": "test-only-secret",
        "SQLALCHEMY_DATABASE_URI": "sqlite:///" + str(tmp_path / "test.sqlite"),
        "WTF_CSRF_ENABLED": False,
    })
    with app.app_context():
        db.create_all()
        db.session.add(AdminUser(username="admin", password_hash=generate_password_hash("test-password")))
        db.session.commit()
    with app.test_client() as client:
        yield client


def test_health_and_public_books(client):
    assert client.get("/health").json == {"status": "ok"}
    assert client.get("/books").status_code == 200


def test_admin_required(client):
    assert client.get("/books/new").status_code == 302
    assert client.get("/users").status_code == 302
    assert client.get("/borrows").status_code == 302
    assert client.get("/auth/signup").status_code == 302


def test_login_and_book_with_zero_stock(client):
    response = client.post("/auth/login", data={"username": "admin", "password": "test-password"})
    assert response.status_code == 302
    response = client.post("/books/new", data={
        "title": "Test", "author": "Author", "genre": "Programming", "stock": "0"
    })
    assert response.status_code == 302
    assert b"Test" in client.get("/books").data


def test_untrusted_logout_requires_login(client):
    assert client.post("/auth/logout").status_code == 302
