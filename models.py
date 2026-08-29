from datetime import datetime

from extensions import db


class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)

    borrows = db.relationship("Borrow", back_populates="user", lazy=True)

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email!r}>"


class Book(db.Model):
    __tablename__ = "books"

    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)

    borrows = db.relationship("Borrow", back_populates="book", lazy=True)

    def __repr__(self):
        return f"<Book book_id={self.book_id} title={self.title!r}>"


class Borrow(db.Model):
    __tablename__ = "borrows"

    borrows_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.book_id"), nullable=False)
    borrowed_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    returned_at = db.Column(db.DateTime, nullable=True)

    user = db.relationship("User", back_populates="borrows")
    book = db.relationship("Book", back_populates="borrows")

    def __repr__(self):
        return (
            f"<Borrow borrows_id={self.borrows_id} "
            f"user_id={self.user_id} book_id={self.book_id}>"
        )


class AdminUser(db.Model):
    __tablename__ = "admin_users"

    admin_user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<AdminUser admin_user_id={self.admin_user_id} username={self.username!r}>"
