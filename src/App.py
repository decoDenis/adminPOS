from flask import Flask, render_template, request,redirect, url_for, flash
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__)

#conexion a mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Fase2'
app.config['MYSQL_DB'] = 'adminpos'
mysql = MySQL(app)

#configuraciones
app.secret_key = 'mysecretkey'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pagina2')
def pagina2():
    return render_template('pagina2.html')    

@app.route('/nuevo_usuario')
def nuevo_usuario():
    return render_template('registrousuario.html')  

@app.route('/login')
def login():
    return render_template('login.html') 

@app.route('/recuperar_password')
def recuperar_password():
    return render_template('recuperar-password.html')

@app.route('/principal')
def principal():
    return render_template('principal.html')                

@app.route('/registro', methods=['POST'])
def registro_usuario():
    if request.method == 'POST':
        username = request.form['user_name']
        useremail = request.form['user_email']
        userpass = request.form['user_pass']
        userroll = request.form['user_roll']
        #funcion cursor para crear la conexion a la bd
        cur = mysql.connection.cursor()
        #escribir la consulta
        #cur.execute('INSERT INTO  usuarios (nombre, rol, )')
        cur.execute('INSERT INTO usuarios (nombre, rol, email, password) VALUES (%s, %s, %s, %s)', (username, userroll, useremail, userpass))
        #ejecutar la consulta
        mysql.connection.commit()
        flash('Usuario creado exitosamente')
        return redirect(url_for('login'))

@app.route('/Lista_usuarios')
def Lista_usuarios():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuarios')
    data = cur.fetchall()
    return render_template('lista_usuarios.html', users=data) 

@app.route('/delete_user/<string:id>')
def delete_user(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM usuarios WHERE idUsuarios = {0}'.format(id))
    mysql.connection.commit()
    flash('Se elimino contacto')
    return redirect(url_for('Lista_usuarios'))     

@app.route('/update_user/<string:id>',methods=['GET', 'POST'])
def update_user(id):
    if request.method == 'POST':
        roll = request.form['roll']
        estado = request.form['estado']

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE usuarios
            SET rol = %s,
                estado = %s
            WHERE idUsuarios = %s    
        """, (roll, estado, id))
        mysql.connection.commit()
        flash('Registro actualizado')
        return redirect(url_for('Lista_usuarios')) 

if __name__ == "__main__":
    app.run(port=3000, debug=True)


