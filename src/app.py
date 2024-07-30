from flask import Flask, flash, jsonify, redirect, request, url_for
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
        nombre_completo = request.form['nombre_completo']
        rol = 'user'
        print(correo,password,nombre_completo,rol)
        new_user = ModelUser.register_user(db,correo,password,nombre_completo,rol)
        return redirect(url_for('login'))
    else:
        return render_template('auth/signup.html')   


@app.route('/check_db', methods=['GET'])
def check_db():
    try:
        # Crear un cursor y ejecutar una consulta simple
        cursor = db.connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()

        if result:
            return jsonify({"status": "success", "message": "Database connection is successful!"}), 200
        else:
            return jsonify({"status": "error", "message": "Database query failed!"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


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