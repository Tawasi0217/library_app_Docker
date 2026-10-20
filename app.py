import os
import secrets

from flask import Flask, jsonify, render_template, g
from flask_login import current_user
from flask_wtf.csrf import CSRFError

from extensions import csrf, db, login_manager


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY"),
        SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL", "sqlite:///library.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    if config:
        app.config.update(config)

    if not app.config.get("SECRET_KEY"):
        if os.environ.get("APP_ENV") == "production":
            raise RuntimeError("Set SECRET_KEY before starting the production server")
        app.config["SECRET_KEY"] = secrets.token_hex(32)

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "この操作には管理者ログインが必要です。"

    from models import AdminUser
    from blueprints.auth import auth_bp
    from blueprints.books import books_bp
    from blueprints.borrows import borrows_bp
    from blueprints.users import users_bp

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return db.session.get(AdminUser, int(user_id))
        except (TypeError, ValueError):
            return None

    app.register_blueprint(auth_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(borrows_bp)

    @app.before_request
    def load_admin_user():
        g.admin_user = current_user if current_user.is_authenticated else None

    @app.template_filter("datetime_jp")
    def datetime_jp(value):
        return value.strftime("%Y-%m-%d %H:%M") if value else "-"

    @app.template_filter("stock_status")
    def stock_status(stock):
        return "貸出可能" if stock > 0 else "在庫なし"

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.errorhandler(404)
    def not_found(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        db.session.rollback()
        return render_template("errors/500.html"), 500

    @app.errorhandler(CSRFError)
    def csrf_error(error):
        return "不正または期限切れのフォームです。再読み込みしてください。", 400

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5000)
