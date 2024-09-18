from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

# parámetros
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT'))
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

# el conector:
mysql = MySQL(app)


@app.route('/')
def form():
    ''' Función que devuelve la lista de películas '''
    cursor = mysql.connection.cursor()  # conectarme a la base de datos
    cursor.execute(''' SELECT nombre, duracion, genero from peliculas''')
    data = cursor.fetchall()
    cursor.close()
    return render_template('index.html', data=data)


@app.route('/pelicula', methods=['POST', 'GET'])
def pelicula():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()  # conectarme a la base de datos
        cursor.execute(''' SELECT nombre, duracion, genero from peliculas''')
        data = cursor.fetchall()
        cursor.close()
        return render_template('index.html', data=data)
    if request.method == 'POST':
        nombre : str = request.form['nombre']
        duracion : int = request.form['duracion']
        genero : str = request.form['genero']
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO peliculas (nombre, duracion, genero) VALUES (%s, %s, %s)''', (nombre, duracion, genero))
        mysql.connection.commit()
        cursor.close()
        return redirect('/')


@app.route('/eliminar', methods=['POST'])
def delete():
    nombre : str = request.form.get('nombre')
    cursor = mysql.connection.cursor()
    cursor.execute(''' DELETE from peliculas WHERE nombre LIKE %s''', (nombre, ))
    mysql.connection.commit()
    cursor.close()
    return redirect('/')


if __name__ == '__main__':
    app.run()
