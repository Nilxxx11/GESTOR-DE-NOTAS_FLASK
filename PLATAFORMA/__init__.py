from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# db para que podamos usarlo más tarde los metodos de la libreria SQLAlchemy en nuestros modelos
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
#La llave secreta para mantener seguras las sesiones del lado del cliente
    app.config['SECRET_KEY'] = 'dDfUfgfEWL'
#SQLALCHEMY_DATABASE_URI se usa para la conexion con la base de datos SQLITE    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

# modelo para rutas de autenticación en nuestra aplicación
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

#modelo para rutas de NO autenticación en nuestra aplicación
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    #Esta clase administra el inicio de sesión y los permisos para la app
    #iniciar y cerrar sesión y recordar las sesiones de los usuarios, evitando el robo de cookies
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # Dado que user_id es la clave principal de nuestra tabla de usuarios, se utiliza en la consulta para el usuario
        return User.query.get(int(user_id))
    return app

