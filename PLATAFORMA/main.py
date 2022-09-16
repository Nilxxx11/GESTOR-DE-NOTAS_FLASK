from flask import Blueprint,render_template
from . import db
from flask_login import login_required, current_user

#Se agrupan las vistas que no requieren autenticacion en main
main = Blueprint('main', __name__)

#vistas a grupar
@main.route('/')
#pagina de inicio
def index():
    return render_template('index.html')

@main.route('/profile')
#perfil del usuario
@login_required #se requiere inicio de sesion para ver perfil
def profile():                             #Aqui se obtiene el nombre del usuario que inicio sesion
    return render_template('profile.html', name=current_user.name)
