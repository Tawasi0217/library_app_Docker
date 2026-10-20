from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from extensions import db
from forms import BookForm, DeleteForm
from models import Book, Borrow

books_bp = Blueprint("books", __name__)


@books_bp.get("/")
@books_bp.get("/books")
def book_list():
    genre = request.args.get("genre", "").strip()
    query = Book.query.order_by(Book.book_id)
    if genre:
        query = query.filter(Book.genre == genre)
    books = query.all()
    genres = [row[0] for row in db.session.query(Book.genre).distinct().order_by(Book.genre)]
    return render_template("books/list.html", books=books, genres=genres, selected_genre=genre)


@books_bp.route("/books/new", methods=["GET", "POST"])
@login_required
def book_create():
    form = BookForm()
    if form.validate_on_submit():
        db.session.add(Book(
            title=form.title.data, author=form.author.data,
            genre=form.genre.data, stock=form.stock.data,
        ))
        db.session.commit()
        flash("本を登録しました。")
        return redirect(url_for("books.book_list"))
    return render_template("books/form.html", form=form, title="本の登録")


@books_bp.route("/books/<int:book_id>/edit", methods=["GET", "POST"])
@login_required
def book_edit(book_id):
    book = db.get_or_404(Book, book_id)
    form = BookForm(obj=book)
    if form.validate_on_submit():
        book.title, book.author, book.genre = form.title.data, form.author.data, form.genre.data
        book.stock = form.stock.data
        db.session.commit()
        flash("本を更新しました。")
        return redirect(url_for("books.book_list"))
    return render_template("books/form.html", form=form, title="本の編集")


@books_bp.route("/books/<int:book_id>/delete", methods=["GET", "POST"])
@login_required
def book_delete(book_id):
    book = db.get_or_404(Book, book_id)
    form = DeleteForm()
    if form.validate_on_submit():
        if Borrow.query.filter_by(book_id=book.book_id).first():
            flash("貸出履歴がある本は削除できません。")
            return redirect(url_for("books.book_list"))
        db.session.delete(book)
        db.session.commit()
        flash("本を削除しました。")
        return redirect(url_for("books.book_list"))
    return render_template("books/delete.html", book=book, form=form)
