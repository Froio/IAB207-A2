from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# Extensions
db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    # Should be set to false in a production environment
    app.debug = True
    app.config['SECRET_KEY'] = 'somesecretkey'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sitedata.sqlite'
    # Limit uploaded image size to ~5 MB
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

    # initialise extensions with flask app
    db.init_app(app)
    bcrypt.init_app(app)
    Bootstrap5(app)

    # initialise the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.scalar(db.select(User).where(User.id == user_id))

    from . import views
    app.register_blueprint(views.main_bp)

    from . import auth
    app.register_blueprint(auth.auth_bp)

    # ── Custom error handlers (Brief req #9) ──
    @app.errorhandler(404)
    def not_found(e):
        return render_template('error.html',
            error_code=404,
            error_message='Page Not Found',
            error_description="The page you're looking for doesn't exist or has been moved."
        ), 404

    @app.errorhandler(500)
    def internal_error(e):
        # Roll back any in-flight DB session so the next request starts clean
        try:
            db.session.rollback()
        except Exception:
            pass
        return render_template('error.html',
            error_code=500,
            error_message='Internal Server Error',
            error_description='Something went wrong on our end. Please try again later.'
        ), 500

    @app.errorhandler(413)
    def payload_too_large(e):
        return render_template('error.html',
            error_code=413,
            error_message='File Too Large',
            error_description='The file you uploaded exceeds the 5 MB limit.'
        ), 413

    # create DB tables automatically
    with app.app_context():
        db.create_all()

    return app
