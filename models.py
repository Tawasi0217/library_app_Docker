from datetime import datetime

from flask_login import UserMixin
from extensions import db


class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    borrows = db.relationship("Borrow", back_populates="user", lazy=True)


class Book(db.Model):
    __tablename__ = "books"
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    borrows = db.relationship("Borrow", back_populates="book", lazy=True)


class Borrow(db.Model):
    __tablename__ = "borrows"
    borrows_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.book_id"), nullable=False)
    borrowed_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    returned_at = db.Column(db.DateTime)
    user = db.relationship("User", back_populates="borrows")
    book = db.relationship("Book", back_populates="borrows")


class AdminUser(UserMixin, db.Model):
    __tablename__ = "admin_users"
    admin_user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)

    def get_id(self):
        return str(self.admin_user_id)
