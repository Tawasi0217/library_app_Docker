from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, url_for

from extensions import db
from forms import BorrowForm
from models import Book, Borrow, User

borrows_bp = Blueprint("borrows", __name__, url_prefix="/borrows")


def populate_borrow_choices(form):
    form.user_id.choices = [(user.user_id, user.name) for user in User.query.order_by(User.name)]
    form.book_id.choices = [
        (book.book_id, f"{book.title} / 在庫 {book.stock}")
        for book in Book.query.filter(Book.stock > 0).order_by(Book.title)
    ]


@borrows_bp.route("/new", methods=["GET", "POST"])
def borrow_create():
    form = BorrowForm()
    populate_borrow_choices(form)

    if form.validate_on_submit():
        book = db.session.get(Book, form.book_id.data)
        if book is None or book.stock <= 0:
            flash("貸出できる在庫がありません。")
            return render_template("borrows/form.html", form=form)

        borrow = Borrow(user_id=form.user_id.data, book_id=form.book_id.data)
        book.stock -= 1
        db.session.add(borrow)
        db.session.commit()
        flash("貸出処理を登録しました。")
        return redirect(url_for("borrows.active_list"))

    return render_template("borrows/form.html", form=form)


@borrows_bp.get("")
def active_list():
    borrows = (
        Borrow.query.filter(Borrow.returned_at.is_(None))
        .join(User)
        .join(Book)
        .order_by(Borrow.borrowed_at.desc())
        .all()
    )
    return render_template("borrows/list.html", borrows=borrows)


@borrows_bp.post("/<int:borrows_id>/return")
def borrow_return(borrows_id):
    borrow = db.get_or_404(Borrow, borrows_id)
    if borrow.returned_at is None:
        borrow.returned_at = datetime.utcnow()
        borrow.book.stock += 1
        db.session.commit()
        flash("返却処理を登録しました。")

    return redirect(url_for("borrows.active_list"))
