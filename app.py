import os

from flask import Flask, g, jsonify, render_template, session

from extensions import db


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "change-this-secret-key"),
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            "DATABASE_URL",
            "sqlite:///library.db",
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if config:
        app.config.update(config)

    db.init_app(app)

    from blueprints.auth import auth_bp
    from blueprints.books import books_bp
    from blueprints.borrows import borrows_bp
    from blueprints.users import users_bp
    from models import AdminUser

    app.register_blueprint(auth_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(borrows_bp)

    @app.before_request
    def load_admin_user():
        admin_user_id = session.get("admin_user_id")
        g.admin_user = (
            db.session.get(AdminUser, admin_user_id) if admin_user_id else None
        )

    @app.template_filter("datetime_jp")
    def datetime_jp(value):
        if value is None:
            return "-"
        return value.strftime("%Y-%m-%d %H:%M")

    @app.template_filter("stock_status")
    def stock_status(stock):
        return "Available" if stock > 0 else "Out of stock"

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

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000, debug=True)
