from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from extensions import db
from forms import DeleteForm, UserForm
from models import Borrow, User

users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.get("")
@login_required
def user_list():
    keyword = request.args.get("q", "").strip()
    query = User.query.order_by(User.user_id)
    if keyword:
        like = f"%{keyword}%"
        query = query.filter(User.name.like(like) | User.email.like(like))
    return render_template("users/list.html", users=query.all(), keyword=keyword)


@users_bp.route("/new", methods=["GET", "POST"])
@login_required
def user_create():
    form = UserForm()
    if form.validate_on_submit():
        db.session.add(User(name=form.name.data, email=form.email.data))
        db.session.commit()
        flash("利用者を登録しました。")
        return redirect(url_for("users.user_list"))
    return render_template("users/form.html", form=form, title="利用者の登録")


@users_bp.route("/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
def user_edit(user_id):
    user = db.get_or_404(User, user_id)
    form = UserForm(obj=user, current_user_id=user.user_id)
    if form.validate_on_submit():
        user.name, user.email = form.name.data, form.email.data
        db.session.commit()
        flash("利用者を更新しました。")
        return redirect(url_for("users.user_list"))
    return render_template("users/form.html", form=form, title="利用者の編集")


@users_bp.route("/<int:user_id>/delete", methods=["GET", "POST"])
@login_required
def user_delete(user_id):
    user = db.get_or_404(User, user_id)
    form = DeleteForm()
    if form.validate_on_submit():
        if Borrow.query.filter_by(user_id=user.user_id).first():
            flash("貸出履歴がある利用者は削除できません。")
            return redirect(url_for("users.user_list"))
        db.session.delete(user)
        db.session.commit()
        flash("利用者を削除しました。")
        return redirect(url_for("users.user_list"))
    return render_template("users/delete.html", user=user, form=form)
