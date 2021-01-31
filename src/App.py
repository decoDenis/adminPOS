from flask import Flask, render_template, request, redirect, url_for, flash, session, json, jsonify,make_response,Markup
from flask_mysqldb import MySQL, MySQLdb
from base64 import b64encode
import qrcode
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import uuid
import os
from pathlib import Path
import datetime
import re
import io
import mysql.connector
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired 
from datetime import timedelta


app = Flask(__name__)

#fecha del servidor
fecha = datetime.datetime.now()

#configuraciones
app.secret_key = 'mysecretkey' 

#conexion a mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Fase2'
app.config['MYSQL_DB'] = 'adminpos'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

originHost="localhost"
originUser="root"
originPass="Fase2"
originDatabase="adminpos"

#segunda conexion a mysql con sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Fase2@localhost/adminpos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#Configuracion para codigo QR
qr = qrcode.QRCode(
    version=1,
    box_size=8,
    border=5
)

#Configuracion de email
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "denisvsnew@gmail.com"
app.config['MAIL_PASSWORD'] = "X01Hd12A."
mail = Mail(app)

s = URLSafeTimedSerializer('mysecretkey')

###########################
#          Rutas          #
# #########################
#Ruta principal del punto de venta.
@app.route('/index')
def index():
    return render_template('index.html')

#Menu principal del sistema.
@app.route('/principal')
def principal():
    if 'username' in session:
        if session['userroll'] == 'admin':
            return render_template('principal.html')
        if session['userroll'] == 'usuario':
            return redirect(url_for('perfil'))
        else:
            return render_template('principal.html')
    else:
        flash("Inicie sesión!")
        return redirect(url_for('login'))

#Mostrar manual de usuario del sistema. 
@app.route('/manual_usuario')
def manual_usuario():
    if 'username' in session:
        return render_template('manual_usuario.html')
    else:
        flash("Inicie sesion.")
        return redirect(url_for('login'))

#Vista para crear nuevo usuario
@app.route('/nuevo_usuario')
def nuevo_usuario():
    if 'username' in session:
        return redirect(url_for('principal'))
    else:
        return render_template('registrousuario.html')  


###########################
#      Tienda online      #
# #########################
#Pagina de tienda principal, muestra productos en general. 
@app.route('/')
@app.route('/pagina2')
def pagina2():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos where activo = %s and existencias >= %s ORDER BY precio_venta DESC LIMIT 16',("1","1"))
    products =  cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.callproc('sp_categories')
    categories =  cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos WHERE activo =%s and existencias >= %s ORDER BY fechaCreacion DESC LIMIT 3',("1","1"))
    ultimos =  cur.fetchall()
    cur.close()

    return render_template('pruebas.html', products=products, categories=categories, ultimos=ultimos)    

#Pagina para ver productos por cantidad
@app.route('/ver_productos/<id>')
def ver_productos(id):

    resultado= int(id)
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos WHERE activo =%s and existencias >= %s ORDER BY nombre ASC LIMIT %s',("1", "1",resultado))
    products =  cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.callproc('sp_categories')
    categories =  cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos WHERE activo =%s and existencias >= %s ORDER BY fechaCreacion DESC LIMIT 3',("1","1"))
    ultimos =  cur.fetchall()
    cur.close()

    return render_template('pruebas.html', products=products, categories=categories, ultimos=ultimos)

#Pagina para ver productos ordenados precio
@app.route('/producto_precio')
def producto_nombre():

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos WHERE activo =%s AND existencias >= %s ORDER BY precio_venta ASC LIMIT 12',("1","1"))
    products =  cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.callproc('sp_categories')
    categories =  cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos WHERE activo =%s AND existencias >= %s ORDER BY fechaCreacion DESC LIMIT 3',("1","1"))
    ultimos =  cur.fetchall()
    cur.close()

    return render_template('pruebas.html', products=products, categories=categories, ultimos=ultimos) 

#Pagina para ver productos por categoria
@app.route('/porcategoria/<id>', methods=['GET','POST'])
def porcategoria(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos WHERE idCategoria =%s AND existencias >= %s ORDER BY precio_venta ASC',(id,"1"))
    products =  cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.callproc('sp_categories')
    categories =  cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos WHERE activo =%s AND existencias >= %s ORDER BY fechaCreacion DESC LIMIT 3',("1","1"))
    ultimos =  cur.fetchall()
    cur.close()

    return render_template('pruebas.html', products=products, categories=categories, ultimos=ultimos) 

#Agregar productos al carrito de compras
@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    try:
        product_id = request.form['product_id']
        cantidad = request.form['quant[1]']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM productos WHERE idProductos=%s',(product_id,))
        product = cur.fetchone()
        cur.close()

        if product_id and cantidad and request.method == 'POST':
            DictItems ={product_id:{'nombre':product['nombre'], 'precio':product['precio_venta'], 'cantidad':cantidad, 'imagen':product['picture'], 'existencias': product['existencias'], 'descripcion': product['descripcion']}}

            if 'listaCompras' in session:
                print(session['listaCompras'])
                if product_id in session['listaCompras']:
                    print("Este producto ya fue agregado a su lista de compra")
                else:
                    session['listaCompras'] = MargerDicts(session['listaCompras'],DictItems)
                    return redirect(request.referrer)
            else:
                session['listaCompras'] = DictItems
                return redirect(request.referrer)

    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

#Carrito de compras manejado con session
@app.route('/lista_compra')
def lista_compra():
    if 'listaCompras' not in session or len(session['listaCompras']) <= 0:
        return redirect(url_for('pagina2'))

    subtotal = 0
    granTotal = 0
    for key, product in session['listaCompras'].items():
        subtotal += float(product['precio']) * int(product['cantidad'])
        impuesto = ("%.2f" % (.06 * float(subtotal)))
        granTotal = float("%.2f" % (float(impuesto) + float(subtotal)))

    return render_template('lista_compras.html', subtotal=subtotal, impuesto=impuesto, granTotal=granTotal)

# Vaciar la session de lista compras si existe
@app.route('/vaciar_lista')
def vaciar_lista():
    try:
        session.pop('listaCompras', None)
        return redirect(url_for('pagina2'))
    except Exception as e:
        print(e)

#Actulizar cantidad de producto
@app.route('/actualizar_lista/<int:id>', methods=['POST'])
def actualizar_lista(id):
    if 'listaCompras' not in session or len(session['listaCompras']) <= 0:
        return redirect(url_for('pagina2'))
    if request.method == 'POST':
        cantidad = request.form.get('quant[1]')
        try:
            session.modified = True
            for key , item in session['listaCompras'].items():
                if int(key) == id:
                    item['cantidad'] = cantidad
                    flash("Cantidad de producto actualizada")
                    return redirect(url_for('lista_compra'))
        except Exception as e:
            print(e)
            return redirect(url_for('lista_compra'))

#Eliminar producto del carrito de compras
@app.route('/eliminar_item/<int:id>')
def eliminar_item(id):
    if 'listaCompras' not in session or len(session['listaCompras']) <= 0:
        return redirect(url_for('pagina2'))
    try:
        session.modified = True
        for key , item in session['listaCompras'].items():
            if int(key) == id:
                session['listaCompras'].pop(key, None)
                return redirect(url_for('lista_compra'))
    except Exception as e:
        print(e)
        return redirect(url_for('lista_compra'))

#Completar la compra si agrego productos al carrito 
@app.route('/orden_cliente')
def orden_cliente():
    if 'username' in session:
        cur2 = mysql.connection.cursor()
        cur2.execute("SELECT * FROM usuarios WHERE idUsuarios = %s and estado = %s",(session['userid'],"activo"))
        usuario = cur2.fetchone()
        cur2.close()

        cur2 = mysql.connection.cursor()
        cur2.execute("SELECT * FROM formasdepago WHERE activo = %s ",("1",))
        formasPago = cur2.fetchall()
        cur2.close()

        if 'listaCompras' not in session or len(session['listaCompras']) <= 0:
            return redirect(url_for('pagina2'))

        subtotal = 0
        granTotal = 0
        for key, product in session['listaCompras'].items():
            subtotal += float(product['precio']) * int(product['cantidad'])
            impuesto = ("%.2f" % (.06 * float(subtotal)))
            granTotal = float("%.2f" % (float(impuesto) + float(subtotal)))

        return render_template('completar_orden.html', usuario=usuario, subtotal=subtotal,impuesto=impuesto,granTotal=granTotal, formasPago=formasPago)
    else:
        flash("Inicie sesion para completar su compra")
        return redirect(url_for('login'))

#Agregar nuevo producto a la lista para manejo con la session 
def MargerDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2,list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False


###########################
#         Backups         #
# #########################
#Realizar respaldo de la base de datos
@app.route('/backup')
def backup():
    if 'username' in session:
        fecha_backup = str(fecha.strftime("%d-%m-%Y_%I_%M_%p"))
        print(fecha_backup)
        nombre = "respaldo_sistema_"+fecha_backup+".sql"
        #El metodo popen permite ejecutar comandos desde python como si se tratase de una terminal, en nuestro caso el comando es mysqldump (Quien se encarga de hacer el respaldo de la BD)
        backup = os.popen("C:/xampp/mysql/bin/mysqldump -u root --password=Fase2 -P 3306 -h 127.0.0.1 adminpos > backups/"+nombre)

        if backup:
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO respaldos (nombre, id_usuario) VALUES (%s, %s)', (nombre, session['userid']))
            mysql.connection.commit()
            cur.close()

            flash("Respaldo generado")
            return redirect(url_for('respaldo_db'))
    else:
        flash("Inicie sesión!")
        return redirect(url_for('login'))

#Listar respaldos de la base de datos realizados.    
@app.route('/respaldo_db')
def respaldo_db():  
    if 'username' in session:
        cur2 = mysql.connection.cursor()
        cur2.execute("SELECT * FROM respaldos")
        datos = cur2.fetchall()
        cur2.close()

        return render_template('backups.html', respaldos=datos)
    else:
        flash("Inicie sesion.")
        return redirect(url_for('login'))


###########################
#        Reportes         #
# #########################
#Reporte de productos agotados
@app.route('/reporte_agotados')
def reporte_agotados():
    if session:
        cur = mysql.connection.cursor()
        cur.callproc('sp_productos_agotados')
        products =  cur.fetchall()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute('select logo from empresas where idEmpresas = %s',("1",))
        empresa =  cur.fetchone()
        cur.close()

        return render_template('reporte_agotados.html', productos=products, empresa=empresa, fecha=fecha)
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

#Reporte de productos con baja existencia
@app.route('/reporte_existencias')
def reporte_existencias():
    if session:
        cur = mysql.connection.cursor()
        cur.callproc('sp_productos_existencias')
        products =  cur.fetchall()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute('select logo from empresas where idEmpresas = %s',("1",))
        empresa =  cur.fetchone()
        cur.close()

        return render_template('reporte_existencias.html', productos=products, empresa=empresa, fecha=fecha)
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

#Reporte ventas por dias
@app.route('/reporte_ventas', methods=['GET','POST'])
def reporte_ventas():
    if session:
        date = request.form['rango']
        [startDate, endDate] = date.split(' - ')

        cur = mysql.connection.cursor()
        cur.callproc('sp_venta_rango', (startDate,endDate))
        ventas =  cur.fetchall()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute('select logo from empresas where idEmpresas = %s',("1",))
        empresa =  cur.fetchone()
        cur.close()

        return render_template('reporte_ventas.html', ventas=ventas, empresa=empresa, fecha=fecha, inicio=startDate, final=endDate)
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

#Reporte de compras por dias
@app.route('/reporte_compras', methods=['GET','POST'])
def reporte_compras():
    if 'username' in session:
        date = request.form['rango_compras']
        [startDate, endDate] = date.split(' - ')

        cur = mysql.connection.cursor()
        cur.callproc('sp_venta_rango', (startDate,endDate))
        compras =  cur.fetchall()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute('select logo from empresas where idEmpresas = %s',("1",))
        empresa =  cur.fetchone()
        cur.close()

        return render_template('reporte_compras.html', compras=compras, empresa=empresa, fecha=fecha, inicio=startDate, final=endDate)
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

#Reporte de ventas por caja
@app.route('/reporte_venta_caja', methods=['GET','POST'])
def reporte_venta_caja():
    if session:
        date = request.form['rango_caja']
        [startDate, endDate] = date.split(' - ')

        cur = mysql.connection.cursor()
        cur.callproc('sp_venta_caja', (startDate,endDate))
        ventas =  cur.fetchall()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute('select logo from empresas where idEmpresas = %s',("1",))
        empresa =  cur.fetchone()
        cur.close()

        return render_template('reporte_venta_caja.html', ventas=ventas, empresa=empresa, fecha=fecha, inicio=startDate, final=endDate)
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

#Reporte de ventas por producto
@app.route('/reporte_venta_producto', methods=['GET','POST'])
def reporte_venta_producto():
    if session:
        date = request.form['rango_producto']
        [startDate, endDate] = date.split(' - ')

        cur = mysql.connection.cursor()
        cur.callproc('sp_venta_producto', (startDate,endDate))
        ventas =  cur.fetchall()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute('select logo from empresas where idEmpresas = %s',("1",))
        empresa =  cur.fetchone()
        cur.close()

        return render_template('reporte_producto.html', ventas=ventas, empresa=empresa, fecha=fecha, inicio=startDate, final=endDate)
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

#Impresion de arqueos de caja
@app.route('/imprimir_arqueo/<id_arqueo>/<id_caja>', methods=['GET','POST'])
def imprimir_arqueo(id_arqueo,id_caja):
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.callproc('sp_reporte_arqueo', (id_arqueo,))
        arqueos =  cur.fetchall()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute('select logo from empresas where idEmpresas = %s',("1",))
        empresa =  cur.fetchone()
        cur.close()

        return render_template('reporte_arqueo.html', arqueos=arqueos, empresa=empresa, fecha=fecha, id_caja=id_caja)
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

#Panel de reportes
@app.route('/reportes')
def reportes():
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT COUNT(*) FROM usuarios WHERE estado =%s',("activo",))
        data =  [v for v in cur.fetchone().values()][0]
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute('SELECT COUNT(*) FROM compras WHERE activo =%s',("1",))
        compras =  [v for v in cur.fetchone().values()][0]
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute('SELECT COUNT(*) FROM ventas WHERE activo =%s',("1",))
        ventas =  [v for v in cur.fetchone().values()][0]
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute('SELECT COUNT(*) FROM clientes WHERE activo =%s',("1",))
        clienteTotal =  [v for v in cur.fetchone().values()][0]
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM clientes WHERE activo =%s ORDER BY fechaCreacion DESC LIMIT 8',("1",))
        clienteCompleto =  cur.fetchall()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM productos where activo = %s order by fechaCreacion DESC limit 5;',("1",))
        productos =  cur.fetchall()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute('SELECT SUM(total) FROM ventas WHERE activo =%s AND DATE(fecha) =%s',("1",fecha.date()))
        diaVentas =  [v for v in cur.fetchone().values()][0]
        cur.close()

        cur2 = mysql.connection.cursor()
        cur2.execute('SELECT SUM(total) FROM compras WHERE activo =%s AND DATE(fecha) =%s',("1",fecha.date()))
        diaCompras =  [v for v in cur2.fetchone().values()][0]
        cur2.close()

        cur3 = mysql.connection.cursor()
        cur3.execute('select count(*) from productos where existencias >= %s and stock_min >= existencias and inventariable = %s and activo = %s;',("1","1","1"))
        inventarioMin =  [v for v in cur3.fetchone().values()][0]
        cur3.close()

        cur4 = mysql.connection.cursor()
        cur4.execute('select count(*) from productos where existencias = %s and activo = %s;',("0","1"))
        agotados =  [v for v in cur4.fetchone().values()][0]
        cur4.close()

        cur = mysql.connection.cursor()
        cur.execute('SELECT sum(total) as totalVenta, DATE_FORMAT(fecha, "%m-%Y") AS mes FROM ventas WHERE activo ="1" GROUP BY DATE_FORMAT(fecha, "%m-%Y") ORDER BY DATE_FORMAT(fecha, "%m-%Y") DESC LIMIT 12')
        datos3 =  cur.fetchall()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute('SELECT sum(total) as totalCompra, DATE_FORMAT(fecha, "%m-%Y") AS mes FROM compras WHERE activo ="1" GROUP BY DATE_FORMAT(fecha, "%m-%Y") ORDER BY DATE_FORMAT(fecha, "%m-%Y") DESC LIMIT 12')
        datos2 =  cur.fetchall()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute('SELECT count(*) as total, DATE_FORMAT(fecha, "%d-%m-%Y") AS mes FROM ventas WHERE activo ="1" GROUP BY DATE_FORMAT(fecha, "%d-%m-%Y") ORDER BY fecha DESC LIMIT 7')
        datos =  cur.fetchall()
        cur.close()

        cur4 = mysql.connection.cursor()
        cur4.execute('SELECT sum(existencias) as inventario FROM productos where activo = %s and inventariable = %s',("1","1"))
        inventario =  [v for v in cur4.fetchone().values()][0]
        cur4.close()

        cur4 = mysql.connection.cursor()
        cur4.execute('select count(*) as total from cajas where activo = %s',("1",))
        cajas =  [v for v in cur4.fetchone().values()][0]
        cur4.close()
        
        cur4 = mysql.connection.cursor()
        cur4.execute('SELECT count(*) FROM productos where activo = %s',("1",))
        productos_total =  [v for v in cur4.fetchone().values()][0]
        cur4.close()

        res = []
        label = []
        res2 = []
        label2 = []
        res3 = []
        label3 = []

        for item in datos:
            res.append(item['mes'])
            label.append(item['total'])
        
        for item in datos2:
            res2.append(item['mes'])
            label2.append(item['totalCompra'])

        for item in datos3:
            res3.append(item['mes'])
            label3.append(item['totalVenta'])

        result = max(label)
        result2 = max(label2)
        result3 = max(label3)

        return render_template('reportes1.html', usuarios=data, compras=compras, ventas=ventas, clientes=clienteTotal, clienteCompleto=clienteCompleto, diaVentas=diaVentas, diaCompras=diaCompras, inventarioMin=inventarioMin, agotados=agotados,  max=result, labels=res, values=label, max2=result2, labels2=res2, values2=label2, max3=result3, labels3=res3, values3=label3, productos=productos, inventario=inventario,productos_total=productos_total, cajas=cajas)
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')


###########################
#     Compra y venta      #
# #########################
#Ver listado de cajas
@app.route('/caja')
def caja():
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM cajas')
        data = cur.fetchall()
        cur.close()

        return render_template('cajas.html', boxes=data) 
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

#Ver registros de compras
@app.route('/compra')
def compra():
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.callproc('listarCompras')
        data = cur.fetchall()
        cur.close()

        return render_template('compra.html', compras=data, fecha=fecha)
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

#Ver registros de venta
@app.route('/venta')
def venta():
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.callproc('listarVentas')
        data = cur.fetchall()
        cur.close()

        return render_template('venta.html', ventas=data, fecha=fecha)
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

#Cancelar venta y actualizar inventario de productos. 
@app.route('/cancelar_venta/<id>', methods=['GET','POST'])
def cancelar_venta(id):
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM detallesventa WHERE idVenta = %s',(id,))
        productos = cur.fetchall()
        cur.close()   

        for producto in productos:
            actualizarStock(producto['idProducto'],producto['cantidad'])
        
        cur2 = mysql.connection.cursor()
        cur2.execute("""UPDATE ventas SET activo = %s WHERE idVentas = %s """, ("0", id))
        mysql.connection.commit()
        cur2.close()

        evento = "Venta cancelada"
        fecha = datetime.datetime.now()
        ip = (request.remote_addr)
        detalles = "Se canceló venta no. "+id
                        
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO logs (id_usuario, evento, fecha, ip, detalles) VALUES (%s, %s, %s, %s, %s)', (session['userid'], evento, fecha, ip, detalles))
        mysql.connection.commit()
        cur.close()
        
        flash('La venta no. '+id+' fue cancelada')
        return redirect(url_for('venta'))
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

#Registrar nueva compra
@app.route('/nueva_compra')
def nueva_compra():
    if 'username' in session:
        if request.method == 'POST':
            pass
        else:
            cur3 = mysql.connection.cursor()
            cur3.execute('SELECT idFormasDePago, nombre, activo FROM formasdepago WHERE activo=%s',("1",))
            formaspago = cur3.fetchall()
            cur3.close()

            cur3 = mysql.connection.cursor()
            cur3.execute('SELECT * FROM proveedores WHERE estado=%s',("1",))
            proveedores = cur3.fetchall()
            cur3.close()

            day_date = fecha.strftime("%d/%m/%Y")
            id_compra = str(uuid.uuid4())
            return render_template('nueva_compra.html', compra=id_compra, day_date=day_date, formaspago=formaspago, proveedores=proveedores)
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

#Registrar nueva venta
@app.route('/nueva_venta')
def nueva_venta():
    if session:
        if request.method == 'POST':
            pass
        else:
            cur3 = mysql.connection.cursor()
            cur3.execute('SELECT * FROM arqueo_caja WHERE id_caja=%s and estatus=%s',(session['caja'],"1"))
            arqueo = cur3.fetchone()
            cur3.close()

            if arqueo:
                caja = session['caja']

                cur3 = mysql.connection.cursor()
                cur3.execute('SELECT idFormasDePago, nombre, activo FROM formasdepago WHERE activo=%s',("1",))
                formaspago = cur3.fetchall()
                cur3.close()

                cur3 = mysql.connection.cursor()
                cur3.execute('SELECT idClientes, nombre FROM clientes WHERE activo=%s',("1",))
                clientes = cur3.fetchall()
                cur3.close()

                cur3 = mysql.connection.cursor()
                cur3.execute('SELECT id_caja, numero_caja, nombre FROM cajas WHERE id_caja=%s',(caja,))
                caja_usuario = cur3.fetchone()
                cur3.close()

                day_date = fecha.strftime("%d/%m/%Y")
                id_venta = str(uuid.uuid4())
                return render_template('nueva_venta.html', compra=id_venta, day_date=day_date, formaspago=formaspago, clientes=clientes, caja=caja_usuario)
            else:
                flash("Aperture caja para realizar transacciones")
                return redirect(url_for('caja'))
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

#Buscar producto por codigo para agregar a venta y compras
@app.route('/buscarPorCodigo/<id>')
def buscarPorCodigo(id):
    if session:
        cur2 = mysql.connection.cursor()
        cur2.execute('SELECT * FROM productos WHERE codigo=%s AND activo=%s',(id,"1"))
        datos = cur2.fetchone()
        cur2.close()

        res = {}
        
        if datos:
            res['datos'] = datos
            res['existe'] = True            
        else:
            res['error'] = "No existe el producto"
            res['existe'] = False

        return jsonify(res)   
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

#guardar compra 
@app.route('/guarda_compra', methods=['POST','GET'])
def guarda_compra():
    if session:
        id_compra = request.form['id_compra']
        total = request.form['total']
        forma_pago = request.form['forma_pago']
        id_usuario = session['userid']
        proveedor = request.form['proveedor']

        resultadoId = insertaCompra(id_compra,total,id_usuario,forma_pago,proveedor)

        if resultadoId:
            resultadoCompra = porCompra(id_compra)
            print(resultadoCompra)
            for row in resultadoCompra:
                cur = mysql.connection.cursor()
                cur.execute('INSERT INTO detallescompra (idCompra, idProducto, precio, cantidad, nombre) VALUES (%s, %s, %s, %s, %s)', (resultadoId, row['id_producto'], row['precio'], row['cantidad'], row['nombre']))
                mysql.connection.commit()
                cur.close()
                actualizarStock(row['id_producto'],row['cantidad'])

            eliminarCompraTemporal(id_compra)

            evento = "Registro de compra"
            fecha = datetime.datetime.now()
            ip = (request.remote_addr)
            detalles = "Se registró  compra no. "+str(resultadoId)
                        
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO logs (id_usuario, evento, fecha, ip, detalles) VALUES (%s, %s, %s, %s, %s)', (session['userid'], evento, fecha, ip, detalles))
            mysql.connection.commit()
            cur.close()

            flash("La compra fue registrada")
        else:
            flash("No se ingresaron valores correctos")
            return redirect(url_for('nueva_compra'))
            
        return redirect(url_for('ver_compra',id_compra=resultadoId))
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

#Guardar venta online
@app.route('/guarda_orden', methods=['POST','GET'])
def guarda_orden():
    if 'username' in session:
        id_venta = str(uuid.uuid4())
        total = request.form['granTotal']
        id_usuario = session['userid']
        forma_pago = request.form['forma_pago']
        id_cliente = 15
        nombre = request.form['name']
        direccion = request.form['address']
        codigo = request.form['post']
        detalle = request.form['w3review']
        impuesto = request.form['impuesto']

        resultadoId = insertaOrden(id_venta, total, id_usuario, forma_pago, id_cliente)

        if resultadoId:
            for key , item in session['listaCompras'].items():
                cur = mysql.connection.cursor()
                cur.execute('INSERT INTO detallesventa (idVenta, idProducto, precio, cantidad, nombre) VALUES (%s, %s, %s, %s, %s)', (resultadoId, key, item['precio'], item['cantidad'], item['nombre']))
                mysql.connection.commit()
                cur.close()
                actualizarStockVenta(key, item['cantidad'])

                guardaOrden(id_usuario,nombre,direccion,codigo,detalle,total,impuesto,resultadoId)
                session.pop('listaCompras', None)
        else:
            flash("Error al registrar compra")
            return redirect(url_for('orden_cliente'))
        
        return redirect(url_for('ver_venta',id_compra=resultadoId))
    else:
        flash("Inicie sesion para completar su compra")
        return redirect(url_for('login'))

#Funcion para guardar orden online
def guardaOrden(id_usuario,nombre,direccion,codigo,detalle,total,costo_envio,id_venta):
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO ordenes_online (id_usuario, nombre_cliente, direccion, codigo_postal, detalle, total, costo_envio,id_venta) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (id_usuario, nombre, direccion, codigo, detalle, total, costo_envio, id_venta))
    mysql.connection.commit()
    cur.close()

#guardar venta cliente establecimiento fisico
@app.route('/guarda_venta', methods=['POST','GET'])
def guarda_venta():
    if session:
        id_compra = request.form['id_compra']
        total = request.form['total']
        forma_pago = request.form['forma_pago']
        id_usuario = session['userid']
        id_caja = session['caja']
        id_cliente = request.form['cliente']
        id_arqueo = request.form['arqueo']

        if id_arqueo == "":
            cur2 = mysql.connection.cursor()
            cur2.execute("SELECT * FROM arqueo_caja WHERE id_caja = %s and estatus = %s", (session['caja'],"1"))
            arqueo = cur2.fetchone()
            cur2.close()
            id_arqueo = arqueo['id_arqueo']

        cur2 = mysql.connection.cursor()
        cur2.execute("SELECT * FROM cajas WHERE id_caja = %s", (id_caja,))
        caja = cur2.fetchone()
        cur2.close()

        correlativo = caja['correlativo']

        resultadoId = insertaVenta(correlativo, total, id_usuario, forma_pago, id_caja, id_cliente, id_arqueo)

        if resultadoId:
            cur = mysql.connection.cursor()
            cur.execute("UPDATE cajas SET correlativo = correlativo + 1 WHERE id_caja = %s",(id_caja,))
            mysql.connection.commit()
            cur.close()

            resultadoCompra = porCompra(id_compra)

            for row in resultadoCompra:
                cur = mysql.connection.cursor()
                cur.execute('INSERT INTO detallesventa (idVenta, idProducto, precio, cantidad, nombre) VALUES (%s, %s, %s, %s, %s)', (resultadoId, row['id_producto'], row['precio'], row['cantidad'], row['nombre']))
                mysql.connection.commit()
                cur.close()
                actualizarStockVenta(row['id_producto'],row['cantidad'])

            eliminarCompraTemporal(id_compra)

            evento = "Registro de venta"
            fecha = datetime.datetime.now()
            ip = (request.remote_addr)
            detalles = "Se registró venta no. "+str(resultadoId)
                        
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO logs (id_usuario, evento, fecha, ip, detalles) VALUES (%s, %s, %s, %s, %s)', (session['userid'], evento, fecha, ip, detalles))
            mysql.connection.commit()
            cur.close()

            flash("La venta fue registrada correctamente")
        else:
            flash("No se ingresaron valores correctos")
            return redirect(url_for('nueva_compra'))
            
        return redirect(url_for('ver_venta',id_compra=resultadoId))
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

#Eliminar producto del detalle de compras y ventas 
@app.route('/eliminar/<id_producto>/<id_compra>')
def eliminar(id_producto, id_compra):
    if session:
        datosExiste = porIdProductoCompra(id_producto, id_compra)

        res ={}

        if datosExiste:
            if datosExiste['cantidad'] > 1:
                cantidad = datosExiste['cantidad'] - 1
                subtotal = cantidad * datosExiste['precio']
                actualizarProductoCompra(id_producto, id_compra, cantidad, subtotal)
            else:
                eliminarProductoCompra(id_producto,id_compra)

        res['datos'] = cargaProductos(id_compra)
        res['total'] = totalProductos(id_compra)
        res['error'] = ""
        return jsonify(res)
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

#Visualizar factura de compra
@app.route('/ver_compra/<id_compra>')
def ver_compra(id_compra):
    if session:
        # id_compra = 33
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM compras WHERE idCompras=%s',(id_compra,))
        datosCompra = cur.fetchall()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM detallescompra WHERE idCompra=%s',(id_compra,))
        detalleCompra = cur.fetchall()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM empresas')
        empresa = cur.fetchall()
        cur.close()

        return render_template('ver_compra.html', compras=datosCompra, detalles=detalleCompra, empresas=empresa)

    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

#Visualizar factura de venta
@app.route('/ver_venta/<id_compra>')
def ver_venta(id_compra):
    if session:
        # id_compra = 33
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM ventas WHERE idVentas=%s',(id_compra,))
        datosVenta = cur.fetchall()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM detallesventa WHERE idVenta=%s',(id_compra,))
        detalleVenta = cur.fetchall()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM empresas')
        empresa = cur.fetchall()
        cur.close()

        return render_template('ver_venta.html', compras=datosVenta, detalles=detalleVenta, empresas=empresa)

    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

#Imprimir factura de compra en pdf
@app.route('/compra_pdf/<id_compra>')
def compra_pdf(id_compra):
    if session:
        # id_compra = 33
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM compras WHERE idCompras=%s',(id_compra,))
        datosCompra = cur.fetchall()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM detallescompra WHERE idCompra=%s',(id_compra,))
        detalleCompra = cur.fetchall()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM empresas')
        empresa = cur.fetchall()
        cur.close()

        return render_template('compra_pdf.html', compras=datosCompra, detalles=detalleCompra, empresas=empresa)

    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

#Imprimir codigo qr de productos
@app.route('/imprimir_qr/<id>',methods=['GET','POST'])
def imprimir_qr(id):
    if session:
        if request.method == 'POST':
            num = int(request.form['qr_producto'])

            if num:
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM productos WHERE idProductos=%s',(id,))
                producto = cur.fetchone()
                cur.close()
            else:
                flash("Ingrese una cantidad valida de tickect")

            return render_template('codigos_qr.html', producto=producto, cantidad=num)
        else:
            return redirect(url_for('lista_producto'))
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

#Imprimmir factura de venta en pdf
@app.route('/venta_pdf/<id_compra>')
def venta_pdf(id_compra):
    if session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM ventas WHERE idVentas=%s',(id_compra,))
        datosCompra = cur.fetchall()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM detallesventa WHERE idVenta=%s',(id_compra,))
        detalleCompra = cur.fetchall()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM empresas')
        empresa = cur.fetchall()
        cur.close()

        return render_template('venta_pdf.html', compras=datosCompra, detalles=detalleCompra, empresas=empresa)
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

#Imprimir ticket de venta 
@app.route('/venta_ticket/<id_venta>')
def venta_ticket(id_venta):
    if session:
        cur = mysql.connection.cursor()
        # cur.execute('SELECT * FROM ventas WHERE idVentas=%s',(id_venta,))
        cur.callproc('ventaCliente',(id_venta,))
        datosCompra = cur.fetchall()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM detallesventa WHERE idVenta=%s',(id_venta,))
        detalleCompra = cur.fetchall()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM empresas')
        empresa = cur.fetchall()
        cur.close()
        ticket = str(uuid.uuid4())

        return render_template('venta_ticket.html', compras=datosCompra, detalles=detalleCompra, empresas=empresa, numero=ticket)
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

#Agregar detalles de compras a la tabla temporal
@app.route('/temporalCompra/<id_producto>/<cantidad>/<id_compra>')
def temporalCompra(id_producto,cantidad,id_compra):
    if session:

        res = {}
        error = ""
        cur2 = mysql.connection.cursor()
        cur2.execute('SELECT * FROM productos WHERE idProductos=%s',(id_producto,))
        producto = cur2.fetchone()
        cur2.close()

        if producto:
            datosExiste = porIdProductoCompra(id_producto,id_compra)
            if datosExiste:
                cantidad = datosExiste['cantidad'] + int(cantidad)
                subTotal = cantidad * datosExiste['precio']

                actualizarProductoCompra(id_producto,id_compra,cantidad,subTotal)
            else:
                subTotal = float(cantidad) * float(producto['precio_compra'])

                cur = mysql.connection.cursor()
                cur.execute('INSERT INTO temporal_compra(folio, id_producto, codigo, nombre, cantidad, precio, subtotal) VALUES (%s,%s,%s,%s,%s,%s,%s)', (id_compra, id_producto, producto['codigo'], producto['nombre'], cantidad, producto['precio_compra'], subTotal))
                mysql.connection.commit()
                cur.close()
        else:
            error = "No existe el producto"

        res['datos'] = cargaProductos(id_compra)
        res['total'] = totalProductos(id_compra)
        res['error'] = error
        return jsonify(res)

    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

#Agregar detalles de ventas a la tabla temporal
@app.route('/temporalVenta/<id_producto>/<cantidad>/<id_compra>')
def temporalVenta(id_producto,cantidad,id_compra):
    if session:

        res = {}
        error = ""
        cur2 = mysql.connection.cursor()
        cur2.execute('SELECT * FROM productos WHERE idProductos=%s',(id_producto,))
        producto = cur2.fetchone()
        cur2.close()

        if producto:
            datosExiste = porIdProductoCompra(id_producto,id_compra)
            if datosExiste:
                cantidad = datosExiste['cantidad'] + int(cantidad)
                subTotal = cantidad * datosExiste['precio']

                actualizarProductoCompra(id_producto,id_compra,cantidad,subTotal)
            else:
                subTotal = float(cantidad) * float(producto['precio_venta'])

                cur = mysql.connection.cursor()
                cur.execute('INSERT INTO temporal_compra(folio, id_producto, codigo, nombre, cantidad, precio, subtotal) VALUES (%s,%s,%s,%s,%s,%s,%s)', (id_compra, id_producto, producto['codigo'], producto['nombre'], cantidad, producto['precio_venta'], subTotal))
                mysql.connection.commit()
                cur.close()
        else:
            error = "No existe el producto"

        res['datos'] = cargaProductos(id_compra)
        res['total'] = totalProductos(id_compra)
        res['error'] = error
        return jsonify(res)

    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

###########################
#       funciones         #
# #########################
def actualizarStock(id_producto,cantidad):
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE productos
        SET existencias = existencias + %s
        WHERE idProductos = %s
    """,(cantidad,id_producto))
    mysql.connection.commit()
    cur.close()

def actualizarStockVenta(id_producto,cantidad):
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE productos
        SET existencias = existencias - %s
        WHERE idProductos = %s
    """,(cantidad,id_producto))
    mysql.connection.commit()
    cur.close()    

def insertaCompra(id_compra,total,id_usuario,forma_pago,id_proveedor):
    curc = mysql.connection.cursor()
    curc.execute('INSERT INTO compras (total, usuario, idProveedor, idFormaPago, folio) VALUES (%s, %s, %s, %s, %s)', (total, id_usuario, id_proveedor, forma_pago, id_compra))
    mysql.connection.commit()
    curc.close()

    return curc.lastrowid

def insertaVenta(id_compra,total,id_usuario,forma_pago,id_caja,id_cliente,id_arqueo):
    curc = mysql.connection.cursor()
    curc.execute('INSERT INTO ventas (total, usuario, idCliente, idFormaPago, folio, id_caja, id_arqueo) VALUES (%s, %s, %s, %s, %s, %s, %s)', (total, id_usuario, id_cliente, forma_pago, id_compra, id_caja, id_arqueo))
    mysql.connection.commit()
    curc.close()

    return curc.lastrowid

def insertaOrden(id_compra,total,id_usuario,forma_pago,id_cliente):
    curc = mysql.connection.cursor()
    curc.execute('INSERT INTO ventas (total, usuario, idCliente, idFormaPago, folio, tipo_venta) VALUES (%s, %s, %s, %s, %s, %s)', (total, id_usuario, id_cliente, forma_pago, id_compra, "2"))
    mysql.connection.commit()
    curc.close()

    return curc.lastrowid

def porIdProductoCompra(id_producto,folio):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM temporal_compra WHERE id_producto=%s AND folio=%s',(id_producto,folio))
    datos = cur.fetchone()
    cur.close() 
    return datos

def porCompra(folio):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM temporal_compra WHERE folio=%s',(folio,))
    datos = cur.fetchall()
    cur.close() 
    return datos

def cargaProductos(id_compra):
    resultado = porCompra(id_compra)
    fila = ""
    numFila = 0

    for result in resultado:
        numFila+=1
            
        fila +="<tr id='fila{}'>".format(numFila)
        fila +="<td>{}</td>".format(numFila)
        fila +="<td>{}</td>".format(result['codigo'])
        fila +="<td>{}</td>".format(result['nombre'])
        fila +="<td>{}</td>".format(result['precio'])
        fila +="<td>{}</td>".format(result['cantidad'])
        fila +="<td>{}</td>".format(result['subtotal'])
        fila +="<td><a onclick=\"eliminaProducto('{}',".format(result['id_producto'])
        fila +="'{}')\"><span class=\"fas fas-fw fa-trash\"></span></a></td>".format(id_compra)
        fila += "</tr>" 
 
    return fila     

def totalProductos(id_compra):
    resultado = porCompra(id_compra)
    total = 0

    for result in resultado:
        total += result['subtotal']

    return total

def actualizarProductoCompra(id_producto,folio,cantidad,subTotal):
    cur3 = mysql.connection.cursor()
    cur3.execute("""
        UPDATE temporal_compra
        SET cantidad = %s,
            subtotal = %s
        WHERE id_producto = %s
        AND folio = %s
    """, (cantidad,subTotal,id_producto,folio))
    mysql.connection.commit()
    cur3.close()

def eliminarProductoCompra(id_producto,folio):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM temporal_compra WHERE folio = %s AND id_producto = %s',(folio,id_producto))
    mysql.connection.commit()
    cur.close()

def eliminarCompraTemporal(folio):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM temporal_compra WHERE folio = %s',(folio,))
    mysql.connection.commit()
    cur.close() 

def cajaArqueo(id_caja):
    cur = mysql.connection.cursor()
    # cur.execute('SELECT * FROM temporal_compra WHERE folio=%s',(folio,))
    cur.callproc('sp_caja_arqueo',(id_caja,))
    datos = cur.fetchall()
    cur.close() 
    return datos

def arqueoUnico(id_arqueo):
    cur = mysql.connection.cursor()
    # cur.execute('SELECT * FROM temporal_compra WHERE folio=%s',(folio,))
    cur.callproc('sp_caja_arqueo',(id_caja,))
    datos = cur.fetchall()
    cur.close() 
    return datos

def totalDia():
    fecha_formato = fecha.date()

    cur = mysql.connection.cursor()
    cur.callproc('sp_total_dia',(fecha_formato,))
    datos = cur.fetchall()
    cur.close() 
    return datos

def totalDiaVenta(id_caja):
    fecha_formato = fecha.date()

    cur = mysql.connection.cursor()
    cur.callproc('sp_total_venta',(fecha_formato,id_caja))
    datos = cur.fetchall()
    cur.close() 
    return datos
    
#no en uso 
@app.route('/autocompleteData', methods=['GET'])
def autocompleteData():

    # search = request.args.get('term')
    data = {}
    returnData = []
    search = "ma"
    print(search)

    cur = mysql.connection.cursor()
    sql = "SELECT idClientes, nombre FROM clientes WHERE nombre LIKE '%{}%'".format(search,)
    cur.execute(sql)
    clientes = cur.fetchall()
    cur.close()

    print(clientes)

    if clientes:
        for cliente in clientes:
            data['id'] = cliente['idClientes']
            data['value'] = cliente['nombre']
            returnData.append(data)
    
        return jsonify(clientes)

#Visualizar datos de la empresa
@app.route('/empresa')
def empresa():
    if session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM empresas')
        data = cur.fetchall()
        cur.close()

        return render_template('empresa.html', items=data)
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')  

#Bitacora de ingreso y salidas del sistema
@app.route('/bitacora')
def bitacora():
    if session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM logs')
        logs = cur.fetchall()
        cur.close()

        return render_template('bitacora.html', logs=logs)
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')              

#Nuevo arqueo de caja
@app.route('/nuevo_arqueo', methods=['GET','POST'])
def nuevo_arqueo():
    if session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT COUNT(*) FROM arqueo_caja WHERE id_caja=%s and estatus = %s',(session['caja'],"1"))    
        datos = [v for v in cur.fetchone().values()][0]
        cur.close() 

        if datos == 0:
            monto = request.form['monto']

            curc = mysql.connection.cursor()
            curc.execute('INSERT INTO arqueo_caja (id_caja, id_usuario, monto_inicial, estatus) VALUES (%s, %s, %s, %s)', (session['caja'], session['userid'], monto, "1"))
            mysql.connection.commit()
            curc.close()

            session['id_arqueo'] = curc.lastrowid

            evento = "Arqueo"
            fecha = datetime.datetime.now()
            ip = (request.remote_addr)
            detalles = "Se arqueo de caja no. "+session['caja']
                        
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO logs (id_usuario, evento, fecha, ip, detalles) VALUES (%s, %s, %s, %s, %s)', (session['userid'], evento, fecha, ip, detalles))
            mysql.connection.commit()
            cur.close()

            return redirect(url_for('caja'))
        else:
            flash("La caja se encuentra aperturada")
            return redirect(url_for('caja'))
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

#cerrar arqueo de caja
@app.route('/cerrar_arqueo/<id_arqueo>/<id_caja>', methods=['GET','POST'])
def cerrar_arqueo(id_caja,id_arqueo):
    if session:
        if request.method == 'POST':
            monto = request.form['monto_final']
            total_venta = request.form['monto_venta']

            cur3 = mysql.connection.cursor()
            cur3.execute("""
                UPDATE arqueo_caja
                SET fecha_fin = %s,
                    monto_final = %s,
                    total_ventas = %s,
                    estatus = %s
                WHERE id_arqueo = %s
            """, (fecha,monto,total_venta,"0",id_arqueo))
            mysql.connection.commit()
            cur3.close()

            evento = "cierre de arqueo"
            fecha = datetime.datetime.now()
            ip = (request.remote_addr)
            detalles = "Cierre de de caja no. "+session['caja']
                        
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO logs (id_usuario, evento, fecha, ip, detalles) VALUES (%s, %s, %s, %s, %s)', (session['userid'], evento, fecha, ip, detalles))
            mysql.connection.commit()
            cur.close()

            flash("Cierre de caja realizado")
            return redirect(url_for('caja'))
        else:
            fecha_formato = fecha.date()

            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM cajas WHERE id_caja=%s',(caja,))
            datos = cur.fetchone()
            cur.close()

            cur = mysql.connection.cursor()
            cur.callproc('sp_total_venta',(fecha_formato,id_caja,id_arqueo))
            total_ventas = cur.fetchall()
            cur.close()

            cur = mysql.connection.cursor()
            cur.callproc('sp_conteo_venta',(fecha_formato,id_caja,id_arqueo))
            conteo_ventas = cur.fetchall()
            cur.close()

            cur = mysql.connection.cursor()
            # cur.callproc('sp_conteo_venta',(fecha_formato,id_caja,id_arqueo))
            cur.execute('select * from arqueo_caja where id_arqueo =%s and id_caja =%s',(id_arqueo,id_caja))
            arqueo_cierre = cur.fetchall()
            cur.close()

            # arqueos = cajaArqueo(id_caja)

            return render_template('cerrar.html', fecha=fecha, caja=datos, id_caja=id_caja, arqueos=arqueo_cierre, total_ventas=total_ventas, conteo=conteo_ventas, id_arqueo=id_arqueo)
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html') 

#Mostrar los arqueos de cierta caja
@app.route('/arqueo_caja/<id_caja>', methods=['GET','POST'])
def arqueo_caja(id_caja):
    if session:
        caja = session['caja']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM cajas WHERE id_caja=%s',(caja,))
        datos = cur.fetchone()
        cur.close() 

        arqueos = cajaArqueo(id_caja)

        return render_template('arqueos.html', id_caja=id_caja, arqueos=arqueos, fecha=fecha, caja=datos)
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')  


###########################
#     Login y Logout      #
# #########################
#Funcion para iniciar sesion y verificar datos de usuarios
@app.route('/login', methods=['POST','GET'])
def login():
    if 'username' in session:
        return redirect(url_for('principal'))
    else:  
        if request.method == 'POST':
            userEmail = request.form['user_email']
            userPassword = request.form['userPassword'].encode('utf-8')
            curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor) #MySQLdb.cursors.DictCursor
            curl.execute("SELECT * FROM usuarios WHERE email=%s", (userEmail,))
            user = curl.fetchone()
            curl.close()

            #Llamado a procedimiento para cargar datos de la empresa
            proc = mysql.connection.cursor()
            proc.execute("call getPos();")
            pos = proc.fetchone()
            proc.close()

            if user:
                if bcrypt.hashpw(userPassword, user['password'].encode('utf-8')) == user['password'].encode('utf-8'):
                    #Tiempo maximo de sesion 
                    session.permanent = True
                    app.permanent_session_lifetime = timedelta(minutes=15)
                    #Variables de sesion guardadas
                    #Datos de usuario
                    session['userid'] = user['idUsuarios']
                    session['username'] = user['nombre']
                    session['email'] = user['email']
                    session['userroll'] = user['rol']
                    session['caja'] = user['id_caja']
                    if user['profilepicture']:
                        session['profilepic'] = user['profilepicture']
                    else:
                        session['profilepic'] = None

                    #Datos de empresa
                    session['posname'] = pos['nombre']
                    session['poslogo'] = pos['logo']

                    id_usuario = session['userid']
                    evento = "Inicio de sesion "
                    fecha = datetime.datetime.now()
                    ip = (request.remote_addr)
                    detalles = request.headers.get('Sec-Ch-Ua')
    
                    cur = mysql.connection.cursor()
                    cur.execute('INSERT INTO logs (id_usuario, evento, fecha, ip, detalles) VALUES (%s, %s, %s, %s, %s)', (id_usuario, evento, fecha, ip, detalles))
                    mysql.connection.commit()
                    cur.close()

                    return redirect(url_for('principal')) #render_template('principal.html')
                else:
                    flash('La contraseña que ingresaste es incorrecta, verifica tus datos.')
                    return render_template('login.html')
            else:
                flash('El usuario ingresado no existe, favor verifica tus datos.')# mensajes
                return render_template('login.html')
        else:
            return render_template('login.html')     

#Cerrar la sesion
@app.route('/logout')
def logout():
    if 'username' in session:
        id_usuario = session['userid']
        evento = "Cierre de sesión"
        fecha = datetime.datetime.now()
        ip = (request.remote_addr)
        detalles = request.headers.get('Sec-Ch-Ua')
    
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO logs (id_usuario, evento, fecha, ip, detalles) VALUES (%s, %s, %s, %s, %s)', (id_usuario, evento, fecha, ip, detalles))
        mysql.connection.commit()
        cur.close()

        session.clear()
        return render_template('index.html')
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')


###########################
#   Recuperar password    #
# #########################
#Recuperar password por medio de correo y token
@app.route('/recuperar_password', methods=['POST','GET'])
def recuperar_password():
    if 'username' in session:
        return redirect(url_for('principal'))
    else:
        if request.method == 'POST':
            email = request.form['userEmail']

            curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor) #MySQLdb.cursors.DictCursor
            curl.execute("SELECT * FROM usuarios WHERE email=%s", (email,))
            user = curl.fetchone()
            curl.close()

            if user:
                token = s.dumps(email, salt='email-confirm')

                cur = mysql.connection.cursor()
                cur.execute("""
                    UPDATE usuarios
                    SET token = %s
                    WHERE email = %s    
                """, (token, email))
                mysql.connection.commit()

                #Enviar email
                msg = Message('Cambio contraseña - AdminPOS', sender='denisvsnew@gmail.com', recipients=[email])
                link = url_for('confirm_email', token=token, _external=True)
                msg.body = 'Hola {}, \r\nPara realizar cambio de su contraseña utilice el siguiente link(Estara disponible por un determinado tiempo): {}'.format(user['nombre'],link)
                mail.send(msg)

                flash("Revise su correo para proceder al cambio de contraseña")
                return redirect(url_for('recuperar_password'))

            else:
                flash("El correo ingresado no existe, verifique sus datos")
                return redirect(url_for('recuperar_password'))
        else:
            return render_template('recuperar-password.html')

#Realizar cambio de contraseña con link enviado al correo
@app.route('/confirm_email/<token>', methods=['POST','GET'])
def confirm_email(token):
    if 'username' in session:
        return redirect(url_for('principal'))
    else:
        u_token = token
        try:
            # El token expira en 15 minutos.
            token = s.loads(token, salt='email-confirm', max_age=900)

            if request.method == 'POST':
                new_pass = request.form['validation2'].encode('utf-8')
                hash_userpass = bcrypt.hashpw(new_pass, bcrypt.gensalt())

                cur = mysql.connection.cursor()
                cur.execute("""
                    UPDATE usuarios
                    SET password = %s
                    WHERE token = %s    
                """, (hash_userpass, u_token))
                mysql.connection.commit()

                id_usuario = session['userid']
                evento = "Cambio de contraseña de usuario."
                fecha = datetime.datetime.now()
                ip = (request.remote_addr)
                detalles = "Usuario "+session['username']+"realizo cambio de contraseña."
            
                cur = mysql.connection.cursor()
                cur.execute('INSERT INTO logs (id_usuario, evento, fecha, ip, detalles) VALUES (%s, %s, %s, %s, %s)', (id_usuario, evento, fecha, ip, detalles))
                mysql.connection.commit()
                cur.close()

                flash("Cambio de contraseña exitoso")
                return redirect(url_for('login'))  
        except SignatureExpired:
            flash("El token expiro")
            return redirect(url_for('recuperar_password'))
        
        return render_template('reset_password.html')


###########################
#     Crear usuarios      #
# #########################
@app.route('/registro', methods=['POST','GET'])
def registro_usuario():
    if 'username' in session:
        return redirect(url_for('principal'))
    else:     
        if request.method == 'POST':
            username = request.form['user_name']
            useremail = request.form['user_email']
            # userpass = request.form['user_pass']
            userroll = request.form['user_roll']
            userpass = request.form['user_pass'].encode('utf-8')
            hash_userpass = bcrypt.hashpw(userpass, bcrypt.gensalt())

            curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor) #MySQLdb.cursors.DictCursor
            curl.execute("SELECT * FROM usuarios WHERE email=%s", (useremail,))
            user = curl.fetchone()
            curl.close()

            if user:
                flash("Usuario ya existe, ingrese con sus datos.")
                return redirect(url_for('registro_usuario'))

            #funcion cursor para crear la conexion a la bd
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO usuarios (nombre, rol, email, password) VALUES (%s, %s, %s, %s)', (username, userroll, useremail, hash_userpass)) #query
            mysql.connection.commit() #ejecutar la consulta y guardar
            cur.close()
            id_usuario = cur.lastrowid

            session['username'] = request.form['user_name']
            session['email'] = request.form['user_email']
            session['userroll'] = request.form['user_roll']
            session['userid'] = id_usuario

            if id_usuario:
                evento = "Creación de nuevo usuario."
                fecha = datetime.datetime.now()
                ip = (request.remote_addr)
                detalles = "Se creo usuario "+session['username']
            
                cur = mysql.connection.cursor()
                cur.execute('INSERT INTO logs (id_usuario, evento, fecha, ip, detalles) VALUES (%s, %s, %s, %s, %s)', (id_usuario, evento, fecha, ip, detalles))
                mysql.connection.commit()
                cur.close()

            flash('Usuario creado exitosamente')# mensajes
            return redirect(url_for('login'))
        else:
            return render_template('registrousuario.html')   


###########################
#     Crear registros     #
# #########################
@app.route('/nuevo_producto', methods=['POST','GET'])
def nuevo_producto():
    if session:     
        if request.method == 'POST':
            
            nombre = request.form['productName']
            precio_venta = request.form['productPriceSale']
            precio_compra = request.form['productPriceBuy']
            id_categoria = request.form['category']
            codigo = request.form['productCode']
            stock_min = request.form['stock']
            inventariable = request.form['inventory']
            id_unidad = request.form['unit']
            descripcion = request.form['inputDescription']
            productImg = request.files['productImg']

            cur2 = mysql.connection.cursor()
            cur2.execute("SELECT codigo FROM productos WHERE codigo = %s", (codigo,))
            code = cur2.fetchall()
            cur2.close()
            
            if id_categoria == "":
                id_categoria = None
            if id_unidad == "":
                id_unidad = None     

            if code:
                flash("Error: Codigo "+ codigo + " ya existe, ingrese nuevo codigo!")
                #return redirect(url_for('nuevo_producto'))
            else:
                #Generar y  guardar codigo QR
                qr.add_data(codigo)
                qr.make(fit=True)
                img = qr.make_image(fill="balck", back_color="white")
                imgqr = str(uuid.uuid1()) + ".png"
                img.save(os.path.join("static/images", imgqr))

                if productImg:
                    #guardar imagen y generar identificador unico para guardar en carpeta images
                    imageName = str(uuid.uuid1()) + os.path.splitext(productImg.filename)[1] 
                    productImg.save(os.path.join("static/images", imageName))

                    cur = mysql.connection.cursor()
                    cur.execute('INSERT INTO productos (nombre, precio_venta, idCategoria, codigo, precio_compra, stock_min, inventariable, id_unidad, descripcion, picture,codigo_qr) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (nombre, precio_venta, id_categoria, codigo, precio_compra, stock_min, inventariable, id_unidad, descripcion, imageName, imgqr))
                    mysql.connection.commit()
                    cur.close()

                    flash('Se agrego nuevo producto')
                    # return redirect(url_for('nuevo_producto'))
                else:
                    cur = mysql.connection.cursor()
                    cur.execute('INSERT INTO productos (nombre, precio_venta, idCategoria, codigo, precio_compra, stock_min, inventariable, id_unidad, descripcion,codigo_qr) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (nombre, precio_venta, id_categoria, codigo, precio_compra, stock_min, inventariable, id_unidad, descripcion, imgqr))
                    mysql.connection.commit()
                    cur.close()
                    flash('Se agrego nuevo producto')

            evento = "Creación de nuevo producto"
            fecha = datetime.datetime.now()
            ip = (request.remote_addr)
            detalles = "Se creo producto "+nombre
            
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO logs (id_usuario, evento, fecha, ip, detalles) VALUES (%s, %s, %s, %s, %s)', (session['userid'], evento, fecha, ip, detalles))
            mysql.connection.commit()
            cur.close()

            return redirect(url_for('nuevo_producto'))

        else:
            cur1 = mysql.connection.cursor()
            cur1.execute('SELECT * FROM categoriasproducto WHERE estado=%s',("1"))
            data1 = cur1.fetchall()
            cur1.close()

            cur2 = mysql.connection.cursor()
            cur2.execute('SELECT * FROM unidades WHERE activo=%s',("1"))
            data2 = cur2.fetchall()
            cur2.close()

            return render_template('nuevo_producto.html', categories=data1, units=data2)    
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

@app.route('/nuevo_proveedor', methods=['POST','GET'])
def nuevo_proveedor():
    if 'username' in session:
        if request.method == 'POST':
            nombre = request.form['pro_name']
            telefono = request.form['pro_phone']
            email = request.form['pro_email']
            direccion = request.form['pro_direccion']

            if nombre and email and direccion:
                cur = mysql.connection.cursor()
                cur.execute('INSERT INTO proveedores (nombre, telefono, email, direccion) VALUES (%s, %s, %s, %s)', (nombre, telefono, email, direccion))
                mysql.connection.commit()
                cur.close()

                evento = "Creación de nuevo proveedor"
                fecha = datetime.datetime.now()
                ip = (request.remote_addr)
                detalles = "Se creo proveedor "+nombre
                
                cur = mysql.connection.cursor()
                cur.execute('INSERT INTO logs (id_usuario, evento, fecha, ip, detalles) VALUES (%s, %s, %s, %s, %s)', (session['userid'], evento, fecha, ip, detalles))
                mysql.connection.commit()
                cur.close()

                flash('Se agrego nuevo proveedor')
                return redirect(url_for('nuevo_proveedor'))
            else:
                flash("Campos Nombre, telefono y direccion son obligarotrios")
                return redirect(url_for('nuevo_proveedor'))
        else:
            return render_template('nuevo_proveedor.html')
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

@app.route('/nuevo_cliente', methods=['POST','GET'])
def nuevo_cliente():
    if session:
        if request.method == 'POST':
            nombre = request.form['clientName']
            telefono = request.form['clientPhone']
            email = request.form['clientEmail']
            direccion = request.form['clientDir']

            if nombre and email and direccion:
                cur = mysql.connection.cursor()
                cur.execute('INSERT INTO clientes (nombre, telefono, email, direccion) VALUES (%s, %s, %s, %s)', (nombre, telefono, email, direccion))
                mysql.connection.commit()
                cur.close()

                evento = "Creación de nuevo cliente"
                fecha = datetime.datetime.now()
                ip = (request.remote_addr)
                detalles = "Se creo cliente "+nombre
                
                cur = mysql.connection.cursor()
                cur.execute('INSERT INTO logs (id_usuario, evento, fecha, ip, detalles) VALUES (%s, %s, %s, %s, %s)', (session['userid'], evento, fecha, ip, detalles))
                mysql.connection.commit()
                cur.close()

                flash('Se agrego nuevo cliente')
                return redirect(url_for('nuevo_cliente'))
            else:
                flash("Campos Nombre, telefono y direccion son obligarotrios")
                return redirect(url_for('nuevo_cliente'))
        else:
            return render_template('nuevo_cliente.html')

    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

@app.route('/nueva_caja', methods=['POST','GET'])
def nueva_caja():
    if session:
        if request.method == 'POST':
            numero_caja = request.form['number']
            nombre = request.form['name']
            correlativo = request.form['sequence']

            if not (numero_caja and nombre):
                flash("Error: El nombre y numero de caja son requeridos")
                return redirect(url_for('caja'))
            else:
                cur = mysql.connection.cursor()
                cur.execute('INSERT INTO cajas (numero_caja, nombre, correlativo) VALUES (%s, %s, %s)', (numero_caja, nombre, correlativo))
                mysql.connection.commit()
                cur.close()

                evento = "Creación de nueva caja"
                fecha = datetime.datetime.now()
                ip = (request.remote_addr)
                detalles = "Se creo caja "+nombre
                
                cur = mysql.connection.cursor()
                cur.execute('INSERT INTO logs (id_usuario, evento, fecha, ip, detalles) VALUES (%s, %s, %s, %s, %s)', (session['userid'], evento, fecha, ip, detalles))
                mysql.connection.commit()
                cur.close()

                flash('Se creo nueva caja')
                return redirect(url_for('caja'))
        else:
            return redirect(url_for('caja'))
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

@app.route('/unidades', methods=['POST','GET'])
def unidades():
    if 'username' in session:
        if request.method == 'POST':
            nombre = request.form['nombre']
            abreviatura = request.form['abreviatura']
            
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO unidades (nombre, abreviatura) VALUES (%s, %s)', (nombre, abreviatura)) #query
            mysql.connection.commit() #ejecutar la consulta y guardar
            cur.close()

            flash('Se creo nueva unidad')# mensajes
            return redirect(url_for('lista_unidades'))
        else:
            return render_template('unidades.html')
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

@app.route('/categorias', methods=['POST','GET'])
def categorias():
    if 'username' in session:
        if request.method == 'POST':
            nombre = request.form['categoryName']
            
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO categoriasproducto (nombre) VALUES (%s)', (nombre,)) #query
            mysql.connection.commit() #ejecutar la consulta y guardar
            cur.close()

            flash('Se agrego nueva categoria')# mensajes
            return redirect(url_for('lista_categorias'))
        else:
            return render_template('categorias.html')
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

@app.route('/nueva_forma', methods=['POST','GET'])
def nueva_forma():
    if 'username' in session:
        if request.method == 'POST':
            nombre = request.form['forma_name']
            
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO formasdepago (nombre) VALUES (%s)', (nombre,)) #query
            mysql.connection.commit() #ejecutar la consulta y guardar
            cur.close()

            evento = "Creación de nueva forma de pago"
            fecha = datetime.datetime.now()
            ip = (request.remote_addr)
            detalles = "Se forma de pago "+nombre
                
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO logs (id_usuario, evento, fecha, ip, detalles) VALUES (%s, %s, %s, %s, %s)', (session['userid'], evento, fecha, ip, detalles))
            mysql.connection.commit()
            cur.close()

            flash('Se agrego nueva forma de pago')# mensajes
            return redirect(url_for('formas_pago'))
        else:
            return redirect(url_for('formas_pago'))
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')


###########################
#    Listar registros     #
# #########################
@app.route('/clientes')
def clientes():
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM clientes WHERE activo=%s', ("1"))
        data = cur.fetchall()
        cur.close()

        return render_template('clientes.html', clients=data) 
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

@app.route('/proveedores')
def proveedores():
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM proveedores WHERE estado=%s', ("1",))
        data = cur.fetchall()
        cur.close()

        return render_template('proveedor.html', proveedores=data) 
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

@app.route('/lista_clientes')
def lista_clientes():
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM clientes')
        data = cur.fetchall()
        cur.close()

        return render_template('lista_clientes.html', clients=data) 
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

@app.route('/Lista_usuarios')
def Lista_usuarios():
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios')
        data = cur.fetchall()
        cur.close()

        cur2 = mysql.connection.cursor()
        cur2.execute('SELECT * FROM cajas WHERE activo=%s AND asignado=%s',("1","0"))
        boxes = cur2.fetchall()
        cur2.close()

        return render_template('lista_usuarios.html', users=data, boxes=boxes) 
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

@app.route('/lista_producto')
def lista_producto():
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM productos WHERE activo=%s',("1"))
        data = cur.fetchall()

        cur.execute('SELECT * FROM categoriasproducto WHERE estado=%s',("1"))
        data2 = cur.fetchall()

        cur.execute('SELECT * FROM unidades WHERE activo=%s',("1"))
        data3 = cur.fetchall()
        cur.close()

        return render_template('lista_producto.html', products=data, categories=data2, units=data3)
    else:
        flash('Ingrese con su usuario')
        return redirect(url_for('login'))

#Lista de unidades
@app.route('/lista_unidades')
def lista_unidades():
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM unidades WHERE activo=%s',("1"))
        data = cur.fetchall()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM unidades WHERE activo=%s',("0"))
        data2 = cur.fetchall()
        cur.close()

        return render_template('unidades.html', units=data ,units2=data2)
    else:
        flash('Ingrese con su usuario')
        return redirect(url_for('login'))

#Vista de categorias 
@app.route('/lista_categorias')
def lista_categorias():
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM categoriasproducto WHERE estado=%s',("1"))
        data = cur.fetchall()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM categoriasproducto WHERE estado=%s',("0"))
        data2 = cur.fetchall()
        cur.close()

        return render_template('categorias.html', categories=data ,categories2=data2)    
    else:
        flash('Ingrese con su usuario')
        return redirect(url_for('login'))

#Formas de pago
@app.route('/formas_pago')
def formas_pago():
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM formasdepago')
        formas = cur.fetchall()
        cur.close()

        return render_template('formas_pago.html', formas=formas)
    else:
        flash('Ingrese con su usuario')
        return redirect(url_for('login'))
    
###########################
#   Eliminar registros    #
# #########################
#Eliminar usuario
@app.route('/delete_user/<id>')
def delete_user(id):
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM usuarios WHERE idUsuarios = {0}'.format(id))
        mysql.connection.commit()

        evento = "Registro eliminado"
        fecha = datetime.datetime.now()
        ip = (request.remote_addr)
        detalles = "Se elimino usuario "+id
                
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO logs (id_usuario, evento, fecha, ip, detalles) VALUES (%s, %s, %s, %s, %s)', (session['userid'], evento, fecha, ip, detalles))
        mysql.connection.commit()
        cur.close()

        flash('Se elimino contacto')
        return redirect(url_for('Lista_usuarios')) 
    else:
        flash('Ingrese con su usuario')
        return redirect(url_for('login')) 

#Eliminar proveedor
@app.route('/delete_proveedor/<id>')
def delete_proveedor(id):
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM proveedores WHERE idProveedores = {0}'.format(id))
        mysql.connection.commit()
        cur.close()

        evento = "Registro eliminado"
        fecha = datetime.datetime.now()
        ip = (request.remote_addr)
        detalles = "Se elimino proveedor "+id
                
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO logs (id_usuario, evento, fecha, ip, detalles) VALUES (%s, %s, %s, %s, %s)', (session['userid'], evento, fecha, ip, detalles))
        mysql.connection.commit()
        cur.close()


        flash('Se elimino Proveedor correctamente')
        return redirect(url_for('proveedores')) 
    else:
        flash('Ingrese con su usuario')
        return redirect(url_for('login')) 

#Eliminado logico de Categorias
@app.route('/delete_category/<id>')
def delete_category(id):
    estado = 0
    
    cur = mysql.connection.cursor()
    cur.execute("""UPDATE categoriasproducto SET estado = %s WHERE idCategoriasProducto = %s """, (estado, id))
    mysql.connection.commit()
    flash('Registro Eliminado!')
    return redirect(url_for('lista_categorias')) 

#Eliminado logico de unidades
@app.route('/delete_unit/<id>')
def delete_unit(id):
    estado = 0
    
    cur = mysql.connection.cursor()
    cur.execute("""UPDATE unidades SET activo = %s WHERE id = %s """, (estado, id))
    mysql.connection.commit()
    flash('Registro Eliminado!')
    return redirect(url_for('lista_unidades'))    

#Eliminado logico de Productos
@app.route('/delete_product/<id>')
def delete_product(id):
    estado = 0
    
    cur = mysql.connection.cursor()
    cur.execute("""UPDATE productos SET activo = %s WHERE idProductos = %s """, (estado, id))
    mysql.connection.commit()
    flash('Registro Eliminado!')
    cur.close()

    evento = "Registro eliminado"
    fecha = datetime.datetime.now()
    ip = (request.remote_addr)
    detalles = "Se elimino producto "+id
                
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO logs (id_usuario, evento, fecha, ip, detalles) VALUES (%s, %s, %s, %s, %s)', (session['userid'], evento, fecha, ip, detalles))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('lista_producto'))        

###################################
#  Visualizar Perfil de usuario   #
# #################################
@app.route('/perfil')
def perfil():
    if 'username' in session:
        id = session['email']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE email=%s',(id,))
        data = cur.fetchall()
        cur.close()

        return render_template('profile.html', items=data) 
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

###################################
#   Actualizar datos de usuario   #
# #################################
@app.route('/update_profile/<id>', methods=['GET','POST'])
def update_profile(id):
    if session:
        if request.method == 'POST':
            nombre = request.form['inputName']
            email = request.form['inputEmail']
            telefono = request.form['userPhone']
            direccion = request.form['direction']
            profilePic = request.files['profilepic']

            if profilePic.filename == "":
                cur = mysql.connection.cursor()
                cur.execute("""
                    UPDATE usuarios 
                    SET nombre = %s,
                        email = %s,
                        telefono = %s,
                        direccion = %s
                    WHERE idUsuarios = %s
                """, (nombre,email,telefono,direccion,id))
                mysql.connection.commit()
                cur.close()

                session['email'] = email

                flash('Se actualizaron datos de pefil')
                return redirect(url_for('perfil'))

            #guardar imagen y generar identificador unico para guardar en carpeta images
            imageName = str(uuid.uuid1()) + os.path.splitext(profilePic.filename)[1] 
            profilePic.save(os.path.join("static/images", imageName))

            cur = mysql.connection.cursor()
            cur.execute("""
                UPDATE usuarios 
                SET nombre = %s,
                    email = %s,
                    telefono = %s,
                    direccion = %s,
                    profilepicture = %s
                WHERE idUsuarios = %s
            """, (nombre,email,telefono,direccion,imageName,id))
            mysql.connection.commit()
            cur.close()

            session['email'] = email

            evento = "Actualización de perfil"
            fecha = datetime.datetime.now()
            ip = (request.remote_addr)
            detalles = "Se actualizo perfil de usuario "+id
                    
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO logs (id_usuario, evento, fecha, ip, detalles) VALUES (%s, %s, %s, %s, %s)', (session['userid'], evento, fecha, ip, detalles))
            mysql.connection.commit()
            cur.close()

            flash('Se actualizaron datos de pefil')
            return redirect(url_for('perfil'))

    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')   

###########################
#  Actualizar registros   #
# #########################
@app.route('/assign_box/<id>', methods=['POST','GET'])
def assign_box(id):
    if session:
        if request.method == 'POST':
            caja = request.form['box']
            usuario = request.form['user_name']
            if caja:
                cur = mysql.connection.cursor()
                cur.execute("""
                    UPDATE usuarios 
                    SET id_caja = %s
                    WHERE idUsuarios = %s
                """, (caja, id))
                mysql.connection.commit()
                cur.close()

                flash("Se asigno caja a usuario "+usuario)
                return redirect(url_for('Lista_usuarios'))
            else:
                flash("No se asigno valor correcto")
                return redirect(url_for('Lista_usuarios'))
        else:
            return redirect(url_for('Lista_usuarios'))
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

@app.route('/update_box/<id>', methods=['POST','GET'])
def update_box(id):
    if session:
        if request.method == 'POST':
            numero_caja = request.form['number2']
            nombre = request.form['name2']
            correlativo = request.form['sequence2']
            estado = request.form['status2']

            if numero_caja and nombre and correlativo:
                cur = mysql.connection.cursor()
                cur.execute("""
                    UPDATE cajas 
                    SET numero_caja = %s,
                        nombre = %s,
                        correlativo = %s,
                        activo = %s
                    WHERE id = %s
                """, (numero_caja,nombre,correlativo, estado,id))
                mysql.connection.commit()
                cur.close()

                flash("Datos de caja no. "+numero_caja+" actualizados")
                return redirect(url_for('caja'))
            else:
                flash("Todos los campos son obligatorios")
                return redirect(url_for('caja'))
        else:
            return redirect(url_for('caja'))
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

@app.route('/update_pos/<id>', methods=['POST','GET'])
def update_pos(id):
    if session:
        if request.method == 'POST':
            nombre = request.form['name']
            telefono = request.form['phone']
            logo = request.files['image']
            direccion = request.form['address']
            rtn = request.form['rtn']
            saludo = request.form['ticket']
            email = request.form['email']

            if logo.filename == "":
                cur = mysql.connection.cursor()
                cur.execute("""
                    UPDATE empresas 
                    SET nombre = %s,
                        telefono = %s,
                        direccion = %s,
                        RTN = %s,
                        saludo = %s,
                        email = %s
                    WHERE idEmpresas = %s
                """, (nombre,telefono,direccion,rtn,saludo,email,id))
                mysql.connection.commit()
                cur.close()

                session['posname'] = nombre

                evento = "Actualización de empresa"
                fecha = datetime.datetime.now()
                ip = (request.remote_addr)
                detalles = "Se actualizo datos de empresa "+id
                        
                cur = mysql.connection.cursor()
                cur.execute('INSERT INTO logs (id_usuario, evento, fecha, ip, detalles) VALUES (%s, %s, %s, %s, %s)', (session['userid'], evento, fecha, ip, detalles))
                mysql.connection.commit()
                cur.close()

                flash('Se actualizaron datos con exito')
                return redirect(url_for('empresa'))
            else:
                #guardar imagen y generar identificador unico para guardar en carpeta images
                imageName = str(uuid.uuid1()) + os.path.splitext(logo.filename)[1] 
                logo.save(os.path.join("static/images", imageName))

                cur = mysql.connection.cursor()
                cur.execute("""
                    UPDATE empresas 
                    SET nombre = %s,
                        telefono = %s,
                        logo = %s,
                        direccion = %s,
                        RTN = %s,
                        saludo = %s,
                        email = %s
                    WHERE idEmpresas = %s
                """, (nombre,telefono,imageName,direccion,rtn,saludo,email,id))
                mysql.connection.commit()
                cur.close()

                session['posname'] = nombre
                session['poslogo'] = imageName

                evento = "Actualización de empresa"
                fecha = datetime.datetime.now()
                ip = (request.remote_addr)
                detalles = "Se actualizo datos de empresa "+id
                        
                cur = mysql.connection.cursor()
                cur.execute('INSERT INTO logs (id_usuario, evento, fecha, ip, detalles) VALUES (%s, %s, %s, %s, %s)', (session['userid'], evento, fecha, ip, detalles))
                mysql.connection.commit()
                cur.close()

                flash('Se actualizaron datos con exito.')
                return redirect(url_for('empresa'))
        else:
            return redirect(url_for('empresa')) 
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

@app.route('/update_client/<id>', methods=['POST','GET'])
def update_client(id):
    if session:
        if request.method == 'POST':
            nombre = request.form['fullname']
            telefono = request.form['phone']
            email = request.form['email']
            direccion = request.form['address']
            activo = request.form['status']

            cur = mysql.connection.cursor()
            cur.execute("""
                UPDATE clientes
                SET nombre = %s,
                    telefono = %s,
                    email = %s,
                    direccion = %s,
                    activo = %s
                WHERE idClientes = %s    
            """, (nombre, telefono, email, direccion, activo, id))
            mysql.connection.commit()

            evento = "Actualización de cliente"
            fecha = datetime.datetime.now()
            ip = (request.remote_addr)
            detalles = "Se actualizó datos de cliente "+nombre
                        
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO logs (id_usuario, evento, fecha, ip, detalles) VALUES (%s, %s, %s, %s, %s)', (session['userid'], evento, fecha, ip, detalles))
            mysql.connection.commit()
            cur.close()

            flash("Cliente "+nombre+ " fue actulizado!")
            return redirect(url_for('clientes')) 

        else:
            return redirect(url_for('clientes')) 
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

#Actualizar datos de clientes
@app.route('/update_clients/<id>', methods=['POST','GET'])
def update_clients(id):
    if 'username' in session:
        if request.method == 'POST':
            nombre = request.form['fullname']
            telefono = request.form['phone']
            email = request.form['email']
            direccion = request.form['address']
            activo = request.form['status']

            cur = mysql.connection.cursor()
            cur.execute("""
                UPDATE clientes
                SET nombre = %s,
                    telefono = %s,
                    email = %s,
                    direccion = %s,
                    activo = %s
                WHERE idClientes = %s    
            """, (nombre, telefono, email, direccion, activo, id))
            mysql.connection.commit()

            flash("Cliente "+nombre+ " fue actulizado!")
            return redirect(url_for('lista_clientes')) 

        else:
            return redirect(url_for('lista_clientes')) 
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

#Actualizar datos de proveedores 
@app.route('/update_proveedor/<id>', methods=['POST','GET'])
def update_proveedor(id):
    if 'username' in session:
        if request.method == 'POST':
            nombre = request.form['fullname']
            telefono = request.form['phone']
            email = request.form['email']
            direccion = request.form['address']
            activo = request.form['status']

            cur = mysql.connection.cursor()
            cur.execute("""
                UPDATE proveedores
                SET nombre = %s,
                    telefono = %s,
                    email = %s,
                    estado = %s,
                    direccion = %s
                WHERE idProveedores = %s    
            """, (nombre, telefono, email, activo, direccion, id))
            mysql.connection.commit()

            flash("Proveedor "+nombre+ " fue actulizado!")
            return redirect(url_for('proveedores')) 

        else:
            return redirect(url_for('proveedores')) 
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

@app.route('/update_user/<id>',methods=['GET', 'POST'])
def update_user(id):
    if 'username' in session:
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
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

@app.route('/update_unit/<id>',methods=['GET', 'POST'])
def update_unit(id):
    if 'username' in session:
        if request.method == 'POST':
            nombre = request.form['nombre']
            abreviatura = request.form['abreviatura']
            activo = request.form['activo']

            cur = mysql.connection.cursor()
            cur.execute("""
                UPDATE unidades
                SET nombre = %s,
                    abreviatura = %s,
                    activo = %s
                WHERE id = %s    
            """, (nombre, abreviatura, activo, id))
            mysql.connection.commit()
            flash('Registro actualizado')
            return redirect(url_for('lista_unidades'))
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

@app.route('/update_category/<id>',methods=['GET', 'POST'])
def update_category(id):
    if 'username' in session:
        if request.method == 'POST':
            nombre = request.form['nombre']
            estado = request.form['activo']

            cur = mysql.connection.cursor()
            cur.execute("""
                UPDATE categoriasproducto
                SET nombre = %s,
                    estado = %s
                WHERE idCategoriasProducto = %s    
            """, (nombre, estado, id))
            mysql.connection.commit()
            cur.close()

            flash('Registro actualizado')
            return redirect(url_for('lista_categorias'))
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

@app.route('/update_forma/<id>',methods=['GET', 'POST'])
def update_forma(id):
    if 'username' in session:
        if request.method == 'POST':
            nombre = request.form['un_forma']
            estado = request.form['us_forma']

            cur = mysql.connection.cursor()
            cur.execute("""
                UPDATE formasdepago
                SET nombre = %s,
                    activo = %s
                WHERE idFormasDePago = %s    
            """, (nombre, estado, id))
            mysql.connection.commit()
            cur.close()

            flash('Registro actualizado')
            return redirect(url_for('formas_pago'))
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

@app.route('/update_product/<id>',methods=['GET', 'POST'])
def update_product(id):
    if 'username' in session:
        if request.method == 'POST':
            nombre = request.form['name']
            codigo = request.form['code']
            precio_venta = request.form['price1']
            precio_compra = request.form['price2']
            idCategoria = request.form['category']
            id_unidad = request.form['unit']
            stock_min = request.form['stock']
            picture = request.files['imagen1']
            descripcion = request.form['inputDescription']
            inventariable = request.form['store']
            
            if idCategoria == "None":
                idCategoria = None

            if id_unidad == "None":
                id_unidad = None  

            if picture:
                #guardar imagen y generar identificador unico para guardar en carpeta images
                imageName = str(uuid.uuid1()) + os.path.splitext(picture.filename)[1] 
                picture.save(os.path.join("static/images", imageName))

                cur = mysql.connection.cursor()
                cur.execute("""
                    UPDATE productos
                    SET nombre = %s,
                        precio_venta = %s, 
                        idCategoria = %s,
                        codigo = %s,
                        precio_compra = %s,
                        stock_min = %s,
                        inventariable = %s,
                        id_unidad = %s,
                        descripcion = %s,
                        picture = %s
                    WHERE idProductos = %s    
                """, (nombre, precio_venta, idCategoria, codigo, precio_compra, stock_min, inventariable, id_unidad, descripcion, imageName, id))
                mysql.connection.commit()
                cur.close()
            else:
                cur = mysql.connection.cursor()
                cur.execute("""
                    UPDATE productos
                    SET nombre = %s,
                        precio_venta = %s, 
                        idCategoria = %s,
                        codigo = %s,
                        precio_compra = %s,
                        stock_min = %s,
                        inventariable = %s,
                        id_unidad = %s,
                        descripcion = %s
                    WHERE idProductos = %s    
                """, (nombre, precio_venta, idCategoria, codigo, precio_compra, stock_min, inventariable, id_unidad, descripcion, id))
                mysql.connection.commit()
                cur.close()

            flash('Registro actualizado')
            return redirect(url_for('lista_producto'))
        else:
            print("metodo get ejecutado")
            return redirect(url_for('lista_producto'))
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

@app.route('/update_password/<id>', methods=['POST','GET'])
def update_password(id):
    if 'username' in session:
        if request.method == 'POST':
            userPassword = request.form['validation1'].encode('utf-8')
            new_pass = request.form['validation2'].encode('utf-8')
            hash_userpass = bcrypt.hashpw(new_pass, bcrypt.gensalt())

            curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            curl.execute("SELECT * FROM usuarios WHERE idUsuarios=%s", (id,))
            user = curl.fetchone()
            curl.close()

            if user:
                if bcrypt.hashpw(userPassword, user['password'].encode('utf-8')) == user['password'].encode('utf-8'):
                    cur = mysql.connection.cursor()
                    cur.execute("""
                        UPDATE usuarios
                        SET password = %s
                        WHERE idUsuarios = %s    
                    """, (hash_userpass, id))
                    mysql.connection.commit()
                    cur.close()

                    flash('La contraseña fue actualizada correctamente')

                    return redirect(url_for('perfil'))
                else:
                    flash('La contraseña actual es incorrecta, verifica tus datos.')
                    return render_template('profile.html')   
            else:
                flash("Error: sin conexión a base de datos")
                return redirect(url_for('perfil'))
        else:
            return redirect(url_for('perfil'))
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

if __name__ == "__main__":
    app.run(port=3000, debug=True)

