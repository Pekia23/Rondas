from flask import Flask, flash, redirect, request, url_for
from flask.templating import render_template
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager,login_user,logout_user,login_required

from config import config
#models
from models.ModelUser import ModelUser
#entities
from models.entities.User import User

app = Flask(__name__)
db = MySQL(app)
csrf = CSRFProtect()
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
                return redirect(url_for('home'))
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
    
@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/protected')
@login_required
def protected():
    return "<h1> area restigida, solo personal autorizado XD </h1>"

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        nombre_completo = request.form['nombre_completo']
        fullname = nombre_completo.title()
        rol = 'user'
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