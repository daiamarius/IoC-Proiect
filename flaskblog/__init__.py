from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config
from flask_assets import Bundle, Environment

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    assets = Environment(app)
    js = Bundle('js/jquery.js','js/popper.min.js','js/bootstrap.min.js','js/chosen.jquery.min.js',
                'js/codemirror.js', 'js/codemirrorscroll.js', output='js/combined.js')
    assets.register('main_js',js)
    css = Bundle('css/bootstrap.css', 'css/main.css', 'css/fontawesome.css',
                'css/chosen.css', 'css/codemirror.css', output='css/combined.css')
    assets.register('main_css',css)

    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
