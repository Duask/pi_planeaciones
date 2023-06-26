from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import config
from models.ModelUser import ModelUser, get_image_url
from models.entities.User import User
from datetime import datetime as t

app = Flask(__name__)

csrf = CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app)

#here we're getting the user data

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

#here we assign the home page

@app.route('/')
def index():
    return redirect(url_for('login'))

#this is the logical part of the login

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User(0, request.form['username'], request.form['password'])
        
        logged_user = ModelUser.login(db, user, table='users')

        if logged_user is None:
            logged_user = ModelUser.login(db, user, table='maestros')

        if logged_user is not None:
            if logged_user is not None:
                login_user(logged_user)
                    
                if logged_user.user_type == 'Administrador':
                    if logged_user.rango == 1:
                        return redirect(url_for('home_sadmin'))
                    elif logged_user.rango == 2:
                        return redirect(url_for('inicio'))
                elif logged_user.user_type == 'Maestro':
                     return redirect(url_for('inicio'))
                else:
                    flash("Tipo de usuario no valido...")
            else:
                flash("Contraseña incorrecta...")
        else:
            flash("Usuario no encontrado...")
        
        return render_template('auth/login.html')
    
    else:
        return render_template('auth/login.html')


#these are the routes to the pages 

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/home_user')
@login_required
def home_user():
    if current_user.user_type == "Maestro":
        return render_template('user/home.html')
    else:
        protected()

@app.route('/home_sadmin')
@login_required
def home_sadmin():
    if current_user.rango == 1:
        return render_template('superAdmin/home.html')
    else:
        protected()

@app.route('/home_admin', methods=['GET', 'POST'])
@login_required
def home_admin():
    if current_user.user_type == "Administrador" and current_user.rango == 2:
        return render_template('admin/home.html')
    else:
        return protected()
    

@app.route('/register')
@login_required
def register():
    if current_user.user_type == "Administrador":
        sql = "SELECT * FROM `maestros`;"
        cursor = db.connection.cursor()
        cursor.execute(sql)
        maestros = cursor.fetchall()
        #print(maestros)
        return render_template('admin/register.html', maestros=maestros)
    
    else:
        return protected()
    
@app.route('/protected')
@login_required
def protected():
    return render_template('admin/protected.html')


@app.route('/inicio')
@login_required
def inicio():
    return render_template('index.html')

@app.route('/admins')
@login_required
def admins():
    if current_user.user_type == "Administrador" and current_user.rango == 1:
        return render_template('superAdmin/admins.html')
    else:
        return protected()
    
@app.route('/carreras')
@login_required
def carreras():
    if current_user.user_type == "Administrador" and current_user.rango == 1:
        return render_template('superAdmin/careers.html')
    else:
        return protected()
    
@app.route('/especialidades')
@login_required
def especialidades():
    if current_user.user_type == "Administrador" and current_user.rango == 1:
        cursor = db.connection.cursor()
        cursor.execute("SELECT * FROM `areas`;")
        special = cursor.fetchall()
        cursor.close()
        return render_template('superAdmin/specialties.html', special=special)
    else:
        return protected()

@app.route('/Recuperar')
def recuperar():
    return render_template('auth/recuperar.html')

#this code is to upload data to the db

@app.route('/store', methods=['POST'])
@login_required
def store():
    name = request.form['txtnombre']
    lastN = request.form['txtapellido']
    correo = request.form['txtcorreo']
    clase = request.form['txtmateria']
    number = request.form['txtnumero']
    passw = request.form['txtpasword']
    hashed_password = User.password(passw)
    image = request.files['txtImage']
    now = t.now()
    time = now.strftime("%Y%H%M%S")
    if image.filename != '':
        newName = time+image.filename
        image.save("static/images/"+newName)

    
    """cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM `maestros` WHERE `correo` = %s;", (correo,))
    existing_maestro = cursor.fetchone()
    cursor.close()

    if existing_maestro:
        flash('Ya existe un registro con el mismo correo.', 'error')
        return redirect(url_for('register')) """

    
    sql = "INSERT INTO `maestros` (`idMaestro`, `Nombres`, `Apellidos`, `Materia`, `numero`,`password`,`imagen`,`correo`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s);"
    datos = (name, lastN, clase, number, hashed_password, newName, correo)
    cursor = db.connection.cursor()
    cursor.execute(sql, datos)
    db.connection.commit()
    cursor.close()

    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM `maestros`;")
    maestros = cursor.fetchall()
    cursor.close()

    return render_template('admin/register.html', maestros=maestros)

#areas

@app.route('/area', methods=['POST'])
@login_required
def area():
    name = request.form['txtnombre']
    image_url = get_image_url(name)

    sql = "INSERT INTO `areas` (`aName`, `urlA`) VALUES (%s, %s);"
    datos = (name, image_url,)
    cursor = db.connection.cursor()
    cursor.execute(sql, datos)
    db.connection.commit()
    cursor.close()
    
    return redirect(url_for('especialidades'))

@app.route('/area/<int:area_id>', methods=['GET'])
@login_required
def delete_area(area_id):
    cursor = db.connection.cursor()
    cursor.execute("DELETE FROM `areas` WHERE `idArea` = %s;", (area_id,))
    db.connection.commit()
    cursor.close()


    return redirect(url_for('especialidades'))



#here just i have the error 404 

def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Página no encontrada</h1>", 404

#conexion para encender flask

if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()






