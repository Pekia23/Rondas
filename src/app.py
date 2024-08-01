from flask import Flask, flash, redirect, request, url_for,session
from flask.templating import render_template
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager,login_user,logout_user,login_required
from forms import SearchForm #importar el formulario

from config import config
#models
from models.ModelUser import ModelUser
#entities
from models.entities.User import User

app = Flask(__name__)
db = MySQL(app)
csrf = CSRFProtect(app)
login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db,id)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=="POST":
       user = User(0,request.form["correo"],request.form["password"])
       logged_user= ModelUser.login(db,user)
       if logged_user!=None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('proyecto'))
            else:
                flash("...Credenciales incorrectas...") 
                return render_template('auth/login.html')
       else:
            flash("...Correo no encontrado...") 
            return render_template('auth/login.html') 
    else:
        return render_template('auth/login.html')  

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
    
@app.route('/proyecto', methods=['GET','POST'])
@login_required
def proyecto():
    form = SearchForm()  # Crea una instancia del formulario
    if form.validate_on_submit():
        search = form.Buscar.data
        proyectos = ModelUser.get_proyecto(db, search)
        categorias = ModelUser.get_categoria(db, search)
        
        resultado = []
        if proyectos:
            resultado.extend(proyectos)
        if categorias:
            resultado.extend(categorias)
        
        session['resultado'] = resultado
        return redirect(url_for('buscador', busqueda=search))
    return render_template('proyecto.html', form=form) 

@app.route('/buscador')
@login_required
def buscador():
    return render_template('buscador.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        nombre_completo = request.form['nombre_completo']
        fullname = nombre_completo.title()
        rol = 'user'
        if ModelUser.get_correo(db, correo):
            flash("El correo ya está registrado")
            return render_template('auth/signup.html')
        if password == confirm_password:
            new_user = ModelUser.register_user(db, correo, password, fullname, rol)
            return redirect(url_for('login'))
        else:
            flash("Las contraseñas no coinciden")
            # Pasar los valores de correo y nombre completo a la plantilla
            return render_template('auth/signup.html', correo=correo, nombre_completo=nombre_completo)
    else:
        return render_template('auth/signup.html')    

def status401(error):
    return redirect(url_for('login'))

def status404(error):
    return '<h1>La pagina no se encuentra, buscalo por otro lado</h1>',404

if __name__=='__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status401)
    app.register_error_handler(404, status404)
    app.run()