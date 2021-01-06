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


app = Flask(__name__)

#fecha del servidor
fecha = datetime.datetime.now()

#configuraciones
app.secret_key = 'mysecretkey' 

#conexion a mysql
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'Fase2'
# app.config['MYSQL_DB'] = 'adminpos'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# MySQL configurations
# app.config['MYSQL_DATABASE_USER'] = 'bc71a3b40d6715'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'c0124eb5'
# app.config['MYSQL_DATABASE_DB'] = 'heroku_360389a98465754'
# app.config['MYSQL_DATABASE_HOST'] = 'us-cdbr-iron-east-05.cleardb.net'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Fase2'
app.config['MYSQL_DB'] = 'adminpos'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

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

###########################
#          Rutas          #
# #########################
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/ejemplo')
def ejemplo():
    return render_template('ejemplo.html')

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

@app.route('/imprimir_arqueo/<id_arqueo>/<id_caja>', methods=['GET','POST'])
def imprimir_arqueo(id_arqueo,id_caja):
    if session:
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

@app.route('/respaldo_db')
def respaldo_db():
    os.popen("mysqldump -h 'localhost' -u 'root' -p adminpos > respaldo.sql")

    flash("Respaldo realizado")
    return redirect(url_for('principal'))

@app.route('/')
@app.route('/pagina2')
def pagina2():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos where activo = %s and existencias >= %s ORDER BY precio_venta DESC LIMIT 12',("1","1"))
    products =  cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM categoriasproducto WHERE estado =%s ORDER BY nombre ASC',("1",))
    categories =  cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos WHERE activo =%s ORDER BY fechaCreacion DESC LIMIT 3',("1",))
    ultimos =  cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.callproc('ventaCliente',("10",))
    ventaClientes =  cur.fetchall()
    cur.close()

    return render_template('pruebas.html', products=products, categories=categories, ultimos=ultimos)    

@app.route('/ver_productos')
@app.route('/ver_productos/<id>')
def ver_productos(id):

    resultado= int(id)
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos WHERE activo =%s ORDER BY nombre ASC LIMIT %s',("1",resultado))
    products =  cur.fetchall()
    cur.close()

    cur2 = mysql.connection.cursor()
    cur2.execute('SELECT * FROM categoriasproducto WHERE estado =%s ORDER BY nombre ASC',("1",))
    categories =  cur2.fetchall()
    cur2.close()

    return render_template('pruebas.html', products=products, categories=categories)

@app.route('/producto_precio')
def producto_nombre():

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos WHERE activo =%s AND existencias >= %s ORDER BY precio_venta ASC LIMIT 12',("1","1"))
    products =  cur.fetchall()
    cur.close()

    cur2 = mysql.connection.cursor()
    cur2.execute('SELECT * FROM categoriasproducto WHERE estado =%s ORDER BY nombre ASC',("1",))
    categories =  cur2.fetchall()
    cur2.close()

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos WHERE activo =%s AND existencias >= %s ORDER BY fechaCreacion DESC LIMIT 3',("1","1"))
    ultimos =  cur.fetchall()
    cur.close()

    return render_template('pruebas.html', products=products, categories=categories, ultimos=ultimos) 

@app.route('/porcategoria/<id>', methods=['GET','POST'])
def porcategoria(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos WHERE idCategoria =%s AND existencias >= %s ORDER BY precio_venta ASC',(id,"1"))
    products =  cur.fetchall()
    cur.close()

    cur2 = mysql.connection.cursor()
    cur2.execute('SELECT * FROM categoriasproducto WHERE estado =%s ORDER BY nombre ASC',("1",))
    categories =  cur2.fetchall()
    cur2.close()

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos WHERE activo =%s AND existencias >= %s ORDER BY fechaCreacion DESC LIMIT 3',("1","1"))
    ultimos =  cur.fetchall()
    cur.close()

    return render_template('pruebas.html', products=products, categories=categories, ultimos=ultimos) 

def MargerDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2,list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False

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
                    # for key ,item in session['listaCompras'].items():
                    #     if int(key) == int(product_id):
                    #         if int(item['cantidad']) <= product['existencias']:
                    #             session.modified = True
                    #             item['cantidad'] += 1
                    #         else:
                    #             print("Producto agotado") 
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

        print(formasPago)

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

@app.route('/codigos_barra')
def codigos_barra():
    if session:
        pass
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

@app.route('/nuevo_usuario')
def nuevo_usuario():
    return render_template('registrousuario.html')  

@app.route('/recuperar_password')
def recuperar_password():
    return render_template('recuperar-password.html')

@app.route('/principal')
def principal():
    return render_template('principal.html')

@app.route('/reportes')
def reportes():
    if session:

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

        return render_template('reportes1.html', usuarios=data, compras=compras, ventas=ventas, clientes=clienteTotal, clienteCompleto=clienteCompleto, diaVentas=diaVentas, diaCompras=diaCompras, inventarioMin=inventarioMin, agotados=agotados,  max=result, labels=res, values=label, max2=result2, labels2=res2, values2=label2, max3=result3, labels3=res3, values3=label3, productos=productos, inventario=inventario,productos_total=productos_total)
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

@app.route('/bar')
def bar():

    cur = mysql.connection.cursor()
    cur.execute('SELECT count(*) as total, DATE_FORMAT(fecha, "%d-%m-%Y") AS mes FROM ventas WHERE activo ="1" GROUP BY DATE_FORMAT(fecha, "%d-%m-%Y") ORDER BY fecha ASC')
    datos =  cur.fetchall()
    cur.close()

    res = []
    label = []

    for item in datos:
        res.append(item['mes'])
        label.append(item['total'])

    result = max(label)
    print("The length of the list is", result)

    return render_template('bar_chart.html', title='Bitcoin Monthly Price in USD', max=result, labels=res, values=label)

@app.route('/caja')
def caja():
    if session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM cajas')
        data = cur.fetchall()
        cur.close()

        return render_template('cajas.html', boxes=data) 
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

@app.route('/compra')
def compra():
    if session:
        cur = mysql.connection.cursor()
        # cur.execute('SELECT * FROM compras')
        cur.callproc('listarCompras')
        data = cur.fetchall()
        cur.close()

        return render_template('compra.html', compras=data, fecha=fecha)
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

@app.route('/venta')
def venta():
    if session:
        cur = mysql.connection.cursor()
        # cur.execute('SELECT * FROM ventas')
        cur.callproc('listarVentas')
        data = cur.fetchall()
        cur.close()

        return render_template('venta.html', ventas=data, fecha=fecha)
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

@app.route('/cancelar_venta/<id>', methods=['GET','POST'])
def cancelar_venta(id):

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
    
    flash('La venta no. '+id+' fue canelada')
    return redirect(url_for('venta'))

@app.route('/nueva_compra')
def nueva_compra():
    if session:
        if request.method == 'POST':
            pass
        else:
            cur3 = mysql.connection.cursor()
            cur3.execute('SELECT idFormasDePago, nombre, activo FROM formasdepago WHERE activo=%s',("1",))
            formaspago = cur3.fetchall()
            cur3.close()

            day_date = fecha.strftime("%d/%m/%Y")
            id_compra = str(uuid.uuid4())
            return render_template('nueva_compra.html', compra=id_compra, day_date=day_date, formaspago=formaspago)
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

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

@app.route('/guarda_compra', methods=['POST','GET'])
def guarda_compra():
    if session:
        id_compra = request.form['id_compra']
        total = request.form['total']
        forma_pago = request.form['forma_pago']
        id_usuario = session['userid']

        resultadoId = insertaCompra(id_compra,total,id_usuario,forma_pago)

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
            flash("La compra fue registrada")
        else:
            flash("No se ingresaron valores correctos")
            return redirect(url_for('nueva_compra'))
            
        return redirect(url_for('ver_compra',id_compra=resultadoId))
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

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

def guardaOrden(id_usuario,nombre,direccion,codigo,detalle,total,costo_envio,id_venta):
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO ordenes_online (id_usuario, nombre_cliente, direccion, codigo_postal, detalle, total, costo_envio,id_venta) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (id_usuario, nombre, direccion, codigo, detalle, total, costo_envio, id_venta))
    mysql.connection.commit()
    cur.close()

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
            flash("La venta fue registrada correctamente")
        else:
            flash("No se ingresaron valores correctos")
            return redirect(url_for('nueva_compra'))
            
        return redirect(url_for('ver_venta',id_compra=resultadoId))
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

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

def insertaCompra(id_compra,total,id_usuario,forma_pago):
    curc = mysql.connection.cursor()
    curc.execute('INSERT INTO compras (total, usuario, idFormaPago, folio) VALUES (%s, %s, %s, %s)', (total, id_usuario, forma_pago, id_compra))
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

@app.route('/generaCompraPdf', methods=['GET', 'POST'])
def generaCompraPdf():

    id_compra = 29
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM compras WHERE idCompras=%s',(id_compra,))
    datosCompra = cur.fetchone()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM detallescompra WHERE idCompra=%s',(id_compra,))
    detalleCompra = cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM empresas')
    empresa = cur.fetchall()
    cur.close()

    # pdf = FPDF()
    pdf = FPDF('P', 'mm', 'letter')
    pdf.add_page()
    # fpdf.set_margins(left: float, top: float, right: float = -1)
    pdf.set_margins(10,10,10)
    # fpdf.set_title(title: str)
    pdf.set_title("Factura de compra")
    # pdf.set_font('Arial', 'B', 16)
    pdf.set_font('Arial', 'B', 10)
    # pdf.output('tuto2.pdf', 'F')
    pdf.cell(195,5,"Entrada de productos",0,1,'C')
    pdf.set_font('Arial', 'B', 9)
    # fpdf.image(name, x = None, y = None, w = 0, h = 0, type = '', link = '')
    pdf.image("static/images/imagen-no-disponible.jpg",185,10,20,20)
    pdf.cell(50,5,"",0,1,'L')
    pdf.cell(50,5,"Direccion: "+empresa[4],0,1,'L')
    response = make_response(pdf.output(dest='S').encode('latin-1'))
    # response.headers.set('Content-Disposition', 'attachment', filename=name + '.pdf')
    response.headers.set('Content-Type', 'application/pdf')
    # pdf.output('compra_pdf.pdf', 'I')
    # pdf.output(dest='I').encode('latin-1')

    return response

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

            return redirect(url_for('caja'))
        else:
            flash("La caja se encuentra aperturada")
            return redirect(url_for('caja'))
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

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
    if session:

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
#     Crear usuarios      #
# #########################
@app.route('/registro', methods=['POST','GET'])
def registro_usuario():
    if session:
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

            session['username'] = request.form['user_name']
            session['email'] = request.form['user_email']
            session['userroll'] = request.form['user_roll']

            flash('Usuario creado exitosamente')# mensajes
            return redirect(url_for('principal'))
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

                flash('Se creo nueva caja')
                return redirect(url_for('caja'))
        else:
            return redirect(url_for('caja'))
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

@app.route('/unidades', methods=['POST','GET'])
def unidades():
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

@app.route('/categorias', methods=['POST','GET'])
def categorias():
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


###########################
#    Listar registros     #
# #########################
@app.route('/clientes')
def clientes():
    if session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM clientes WHERE activo=%s', ("1"))
        data = cur.fetchall()
        cur.close()

        return render_template('clientes.html', clients=data) 
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

@app.route('/lista_clientes')
def lista_clientes():
    if session:
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
    if session:
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
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos WHERE activo=%s',("1"))
    data = cur.fetchall()

    cur.execute('SELECT * FROM categoriasproducto WHERE estado=%s',("1"))
    data2 = cur.fetchall()

    cur.execute('SELECT * FROM unidades WHERE activo=%s',("1"))
    data3 = cur.fetchall()
    cur.close()

    return render_template('lista_producto.html', products=data, categories=data2, units=data3)

@app.route('/lista_unidades')
def lista_unidades():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM unidades WHERE activo=%s',("1"))
    data = cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM unidades WHERE activo=%s',("0"))
    data2 = cur.fetchall()
    cur.close()

    return render_template('unidades.html', units=data ,units2=data2)

@app.route('/lista_categorias')
def lista_categorias():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM categoriasproducto WHERE estado=%s',("1"))
    data = cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM categoriasproducto WHERE estado=%s',("0"))
    data2 = cur.fetchall()
    cur.close()

    return render_template('categorias.html', categories=data ,categories2=data2)    
    
###########################
#   Eliminar registros    #
# #########################
@app.route('/delete_user/<id>')
def delete_user(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM usuarios WHERE idUsuarios = {0}'.format(id))
    mysql.connection.commit()
    flash('Se elimino contacto')
    return redirect(url_for('Lista_usuarios')) 

#Eliminado logico de Categorias
@app.route('/delete_category/<id>')
def delete_category(id):
    estado = 0
    
    cur = mysql.connection.cursor()
    cur.execute("""UPDATE categoriasproducto SET estado = %s WHERE idCategoriasProducto = %s """, (estado, id))
    mysql.connection.commit()
    flash('Registro Eliminado!')
    return redirect(url_for('lista_categorias'))    

#Eliminado logico de Productos
@app.route('/delete_product/<id>')
def delete_product(id):
    estado = 0
    
    cur = mysql.connection.cursor()
    cur.execute("""UPDATE productos SET activo = %s WHERE idProductos = %s """, (estado, id))
    mysql.connection.commit()
    flash('Registro Eliminado!')
    return redirect(url_for('lista_producto'))        

###################################
#  Visualizar Perfil de usuario   #
# #################################
@app.route('/perfil')
def perfil():
    if session:
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

            flash("Cliente "+nombre+ " fue actulizado!")
            return redirect(url_for('clientes')) 

        else:
            return redirect(url_for('clientes')) 
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

@app.route('/update_clients/<id>', methods=['POST','GET'])
def update_clients(id):
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

            flash("Cliente "+nombre+ " fue actulizado!")
            return redirect(url_for('lista_clientes')) 

        else:
            return redirect(url_for('lista_clientes')) 
    else:
        flash("Ingrese usuario y contraseña.")
        return render_template('login.html')

@app.route('/update_user/<id>',methods=['GET', 'POST'])
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

@app.route('/update_unit/<id>',methods=['GET', 'POST'])
def update_unit(id):
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

@app.route('/update_category/<id>',methods=['GET', 'POST'])
def update_category(id):
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

@app.route('/update_product/<id>',methods=['GET', 'POST'])
def update_product(id):
    if session:
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
    if session:
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


