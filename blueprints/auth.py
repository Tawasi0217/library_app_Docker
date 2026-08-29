from flask import Blueprint, flash, redirect, render_template, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from extensions import db
from forms import LoginForm, SignupForm
from models import AdminUser

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        admin_user = AdminUser.query.filter_by(username=form.username.data).first()
        if admin_user and check_password_hash(admin_user.password_hash, form.password.data):
            session.clear()
            session["admin_user_id"] = admin_user.admin_user_id
            flash("ログインしました。")
            return redirect(url_for("books.book_list"))

        flash("ユーザー名またはパスワードが違います。")

    return render_template("auth/login.html", form=form)


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        admin_user = AdminUser(
            username=form.username.data,
            password_hash=generate_password_hash(form.password.data),
        )
        db.session.add(admin_user)
        db.session.commit()
        flash("管理者を登録しました。")
        return redirect(url_for("auth.login"))

    return render_template("auth/signup.html", form=form)


@auth_bp.post("/logout")
def logout():
    session.clear()
    flash("ログアウトしました。")
    return redirect(url_for("auth.login"))
