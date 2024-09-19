from flask import Flask, render_template, request, redirect, url_for
import pymysql
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)


# Configura la conexión a la base de datos MySQL con pymysql
def get_db_connection():
    connection = pymysql.connect(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),      # Cambia al usuario de tu base de datos
        password=os.getenv('MYSQL_PASSWORD'), # Cambia a la contraseña de tu base de datos
        db=os.getenv('MYSQL_DB'),  # Cambia al nombre de tu base de datos
        port=int(os.getenv('MYSQL_PORT')),
        cursorclass=pymysql.cursors.DictCursor  # Para obtener los resultados como diccionarios
    )
    return connection


@app.route('/')
def form():
    ''' Función que devuelve la lista de películas '''
    connection = get_db_connection()  # Conectarse a la base de datos
    cursor = connection.cursor()
    cursor.execute(''' SELECT nombre, duracion, genero FROM peliculas ''')
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    print(data)
    return render_template('index.html', data=data)


@app.route('/pelicula', methods=['POST', 'GET'])
def pelicula():
    if request.method == 'GET':
        connection = get_db_connection()  # Conectarse a la base de datos
        cursor = connection.cursor()
        cursor.execute(''' SELECT nombre, duracion, genero FROM peliculas ''')
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('index.html', data=data)

    if request.method == 'POST':
        nombre = request.form['nombre']
        duracion = int(request.form['duracion'])
        genero = request.form['genero']

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(''' 
            INSERT INTO peliculas (nombre, duracion, genero) 
            VALUES (%s, %s, %s)
        ''', (nombre, duracion, genero))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect('/')


@app.route('/eliminar', methods=['POST'])
def delete():
    nombre = request.form.get('nombre')

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(''' DELETE FROM peliculas WHERE nombre LIKE %s ''', (nombre,))
    connection.commit()
    cursor.close()
    connection.close()

    return redirect('/')


if __name__ == '__main__':
    app.run()
