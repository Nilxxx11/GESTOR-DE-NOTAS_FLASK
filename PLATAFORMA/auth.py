from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
from flask_login import login_user, logout_user, login_required
from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')
@auth.route('/signup')
def signup():
    return render_template('signup.html')
@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    
    user = User.query.filter_by(email=email).first() # si esto devuelve un usuario, entonces el correo electrónico ya existe en la base de datos
    
# Si se encuentra un usuario registrado, sera redireccionado a la página de registro nuevamente para que el usuario pueda volver a intentarlo y se le sugerira que vaya a pagina de inicio de sesion
    if user: 
        flash('Usuario Email registrado ')
        return redirect(url_for('auth.signup'))

# se crear un nuevo usuario con los datos del formulario. se Hashea con sha256 la contraseña para que la versión de texto sin formato no se guarde.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # Se añade el nuevo usuario a la base de datos
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))
#Inicio de sesion 
@auth.route('/login', methods=['POST'])
def login_post():
    #Se capturan los datos del formulario
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    #Se consulta si el usuario con su email existe en la base de datos, eligiendo el primero que se encuentre
    user = User.query.filter_by(email=email).first()

    # verificar si el usuario realmente existe
    # tomar la contraseña proporcionada por el usuario, cifrarla y compararla con la contraseña cifrada en la base de datos
    if not user or not check_password_hash(user.password, password):
        flash('Verifica las credenciales e intenta de nuevo.')
        return redirect(url_for('auth.login')) # si el usuario no existe o la contraseña es incorrecta, recargar la página login (inicio de sesion)
    # si la verificación anterior pasa, entonces sabemos que el usuario tiene las credenciales correctas
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))#se redirecciona a la pagina de su perfil
    return redirect(url_for('auth.login'))
