from flask import Flask, app, flash, render_template, request, url_for, redirect, session
from flask_mysqldb import MySQL,MySQLdb
import hashlib






app = Flask(__name__)

app.config['MYSQL_HOST']='kutnpvrhom7lki7u.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER']='eua8ryreprz7pmqe'
app.config['MYSQL_PASSWORD']='rl6oz9bag1ub07g1'
app.config['MYSQL_DB']='icd69vrm68ife5dp'

mysql=MySQL(app)





app.secret_key='mysecretkey'

@app.route('/', methods=['GET','POST'])
def login():
    if request.method=='POST':
        usuario=request.form['inputusuario']
        contra=request.form['inputcontraseña']
        clave=contra.encode('utf-8')
        contraseña=hashlib.md5(clave).hexdigest()
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE usuario=%s',(usuario,))
        data=cursor.fetchall()
        cursor.execute('SELECT * FROM usuarios WHERE contraseña=%s',(contraseña,))
        data2=cursor.fetchall()
        if  data2 and data:
            session['user']=usuario
            return redirect(url_for('registropersonas'))       
        else:
            flash('Usuario o contraseña incorrecto') 
            return render_template('login.html')
      
    else:
        return render_template('login.html')
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/registrolideres')
def registrolideres():
    if 'user' in session:
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT * FROM lideres')
        data2=cursor.fetchall()
        cursor.close()
        return render_template('registrolideres.html',lideres=data2)
    else:
        return 'No ha iniciado sesión'    

@app.route('/registro')
def registropersonas():
    if 'user' in session:
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT * FROM personas')
        data=cursor.fetchall()
        cursor.execute('SELECT * FROM lideres')
        data2=cursor.fetchall()
        cursor.close()
        return render_template('registropersonas.html', personas=data, lideres=data2)
    else:
        return 'No ha iniciado sesión' 
     


@app.route('/aggpersona', methods=['POST'])
def aggpersona():
    if request.method=='POST':
        nombre=request.form['inputnombre']
        apellidos=request.form['inputapellido']
        cedula=request.form['inputcedula']
        telefono=request.form['inputtelefono']
        email=request.form['inputemail']
        lugar_votacion=request.form['inputvotacion']
        mesa=request.form['inputmesa']
        lider=request.form['selectlider']
        municipio=request.form['selectmunicipio']
        barrio=request.form['inputbarrio']
        cursor=mysql.connection.cursor()
        cursor.execute('INSERT INTO personas (nombres, apellidos, cedula, telefono, email, lugar_votacion, mesa, lider, municipio, barrio) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
        (nombre,apellidos,cedula,telefono,email,lugar_votacion,mesa,lider,municipio,barrio))
        mysql.connection.commit()
        flash('Persona agregada exitosamente')
        return redirect(url_for('registropersonas'))
    

@app.route('/agglider', methods=['POST'])
def agglider():
    if request.method=='POST':
        nombre=request.form['nombrelider']
        apellidos=request.form['apellidolider']
        cedula=request.form['cedulalider']
        telefono=request.form['telefonolider']
        municipio=request.form['municipiolider']
        barrio=request.form['barriolider']
        cursor=mysql.connection.cursor()
        cursor.execute('INSERT INTO lideres (nombres, apellidos, cedula, telefono, municipio, barrio) VALUES (%s,%s,%s,%s,%s,%s)',(nombre,apellidos,cedula,telefono,municipio,barrio))
        mysql.connection.commit()

        flash('Líder agregado exitosamente')
        return redirect(url_for('registrolideres'))

@app.route('/eliminar/<string:id>')
def eliminarpersona(id):
    if 'user' in session:
        cursor=mysql.connection.cursor()
        cursor.execute('DELETE FROM personas WHERE id={0}'.format(id))
        print(id)
        mysql.connection.commit()
        flash('Persona eliminada exitosamente')
        return redirect(url_for('registropersonas'))
    else: 'No ha iniciado sesión'

@app.route('/eliminarlider/<string:id>')
def eliminarlider(id):
    if 'user' in session:
        cursor=mysql.connection.cursor()
        cursor.execute('DELETE FROM lideres WHERE id={0}'.format(id))
        mysql.connection.commit()
        flash('Líder eliminado exitosamente')
        return redirect(url_for('registrolideres'))
    else: 'No ha iniciado sesión'


@app.route('/editarpersona/<id>')
def editarpersona(id):
    if 'user' in session:
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT * FROM personas WHERE id={0}'.format(id))
        data=cursor.fetchall()
        cursor.execute('SELECT * FROM lideres')
        data2=cursor.fetchall()
        return render_template('editarpersona.html', personas=data[0],lideres=data2)
    else:
        return "No ha iniciado sesión"

@app.route('/editarlider/<id>')
def editarlider(id):
    if 'user' in session:
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT * FROM lideres WHERE id={0}'.format(id))
        data2=cursor.fetchall()
        return render_template('editarlider.html', lideres=data2[0])
    else:
        return "No ha iniciado sesión"


@app.route('/actualizarpersona/<id>', methods=['POST'])
def actualizarpersona(id):
    
    if request.method=='POST':
        nombre=request.form['inputnombreact']
        apellidos=request.form['inputapellidoact']
        cedula=request.form['inputcedulaact']
        telefono=request.form['inputtelefonoact']
        email=request.form['inputemailact']
        lugar_votacion=request.form['inputvotacionact']
        mesa=request.form['inputmesaact']
        lider=request.form['selectlideract']
        municipio=request.form['selectmunicipioact']
        barrio=request.form['inputbarrioact']
        cursor=mysql.connection.cursor()
        cursor.execute("""UPDATE personas SET nombres=%s, apellidos=%s, cedula=%s, telefono=%s, email=%s, lugar_votacion=%s, mesa=%s, lider=%s, municipio=%s, barrio=%s WHERE id=%s """, 
        (nombre,apellidos,cedula,telefono,email,lugar_votacion,mesa,lider,municipio,barrio,id))
        mysql.connection.commit()
        flash('Persona actualizada exitosamente')
        return redirect(url_for('registropersonas'))
        



@app.route('/actualizarlider/<id2>', methods=['POST'])
def actualizarlider(id2):
    
        if request.method=='POST':
            nombre=request.form['nombrelideract']
            apellidos=request.form['apellidolideract']
            cedula=request.form['cedulalideract']
            telefono=request.form['telefonolideract']
            municipio=request.form['municipiolideract']
            barrio=request.form['barriolideract']
            cursor=mysql.connection.cursor()
            cursor.execute("""UPDATE lideres SET nombres=%s, apellidos=%s, cedula=%s, telefono=%s, municipio=%s, barrio=%s WHERE id=%s """, 
            (nombre,apellidos,cedula,telefono,municipio,barrio,id2))
            mysql.connection.commit()
            flash('Líder actualizado exitosamente')
            return redirect(url_for('registrolideres'))


"""@app.route('/buscarpersona', methods=['POST'])
def buscarpersona():
    if 'user' in session:
     conexion=sqlite3.connect('elecciones.db')
     persona=request.form['buscarpersona']

     print(persona)
     cursor=conexion.cursor()
     cursor.execute("SELECT * FROM personas WHERE nombres LIKE ?",persona[0])
     data=cursor.fetchall()
     print (data)
     conexion.close()
     if cursor.fetchall:
        return render_template('registropersonas.html', buscarpersona=data)
    else:
        return 'No ha iniciado sesión' """
    
    


if __name__=='__main__':
    app.run(debug=True)
