from flask import Flask, jsonify, request, render_template
import mysql.connector

# Inicializa la aplicación Flask
app = Flask(__name__)

# Función para establecer conexión con la base de datos
def connect_db():
    return mysql.connector.connect(
        host='localhost',
        port=8080,
        user='root',
        password='Zrcirconio.29',
        database='prueba'
    )

# Función para ejecutar consultas a la base de datos
def execute_query(query, values=None, fetch=False):
    connection = connect_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, values)
    result = cursor.fetchall() if fetch else connection.commit()
    cursor.close()
    connection.close()
    return result

# Ruta para la página principal (interfaz HTML)
@app.route('/')
def index():
    return render_template('practica2.html')

# Obtener todos los alumnos
@app.route('/alumnos', methods=['GET'])
def get_alumnos():
    alumnos = execute_query("SELECT * FROM alumnos", fetch=True)
    return jsonify(alumnos), 200

# Agregar un nuevo alumno (POST)
@app.route('/alumnos', methods=['POST'])
def add_alumno():
    data = request.json
    execute_query("INSERT INTO alumnos (nombre, telefono, matricula) VALUES (%s, %s, %s)",
                  (data['nombre'], data['telefono'], data['matricula']))
    return jsonify({'message': 'Alumno creado exitosamente'}), 201

# Actualizar un alumno (PUT)
@app.route('/alumnos/<int:id>', methods=['PUT'])
def update_alumno(id):
    data = request.json
    execute_query("UPDATE alumnos SET nombre = %s, telefono = %s, matricula = %s WHERE id = %s",
                  (data['nombre'], data['telefono'], data['matricula'], id))
    return jsonify({'message': 'Alumno actualizado exitosamente'}), 200

# Eliminar un alumno (DELETE)
@app.route('/alumnos/<int:id>', methods=['DELETE'])
def delete_alumno(id):
    execute_query("DELETE FROM alumnos WHERE id = %s", (id,))
    return jsonify({'message': 'Alumno eliminado exitosamente'}), 200

# Verificar que el archivo se ejecute correctamente
if __name__ == "__main__":
    app.run(debug=True)