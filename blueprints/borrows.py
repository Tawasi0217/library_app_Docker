from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required
from sqlalchemy import update

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
@login_required
def borrow_create():
    form = BorrowForm()
    populate_borrow_choices(form)
    if form.validate_on_submit():
        # Atomic stock decrement prevents overselling under concurrent requests.
        result = db.session.execute(
            update(Book).where(Book.book_id == form.book_id.data, Book.stock > 0)
            .values(stock=Book.stock - 1)
        )
        if result.rowcount != 1:
            db.session.rollback()
            flash("貸出できる在庫がありません。")
            return render_template("borrows/form.html", form=form), 409

        db.session.add(Borrow(user_id=form.user_id.data, book_id=form.book_id.data))
        db.session.commit()
        flash("貸出処理を登録しました。")
        return redirect(url_for("borrows.active_list"))
    return render_template("borrows/form.html", form=form)


@borrows_bp.get("")
@login_required
def active_list():
    borrows = (
        Borrow.query.filter(Borrow.returned_at.is_(None))
        .join(User).join(Book).order_by(Borrow.borrowed_at.desc()).all()
    )
    return render_template("borrows/list.html", borrows=borrows)


@borrows_bp.post("/<int:borrows_id>/return")
@login_required
def borrow_return(borrows_id):
    borrow = db.get_or_404(Borrow, borrows_id)
    # A conditional update makes a duplicate return request idempotent.
    result = db.session.execute(
        update(Borrow)
        .where(Borrow.borrows_id == borrows_id, Borrow.returned_at.is_(None))
        .values(returned_at=datetime.utcnow())
    )
    if result.rowcount == 1:
        db.session.execute(
            update(Book).where(Book.book_id == borrow.book_id).values(stock=Book.stock + 1)
        )
        db.session.commit()
        flash("返却処理を登録しました。")
    else:
        db.session.rollback()
    return redirect(url_for("borrows.active_list"))
