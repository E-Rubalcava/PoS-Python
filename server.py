from mysql.connector import connect, Error
from flask import Flask, jsonify

app = Flask(__name__)
# Configuración de la base de datos
db_config = {
    'host': 'localhost',
    'database': 'pos',
    'user': 'root',
    'password': 'password1234',
    'port': 3306
}

def create_db_connection():
    try:
        connection = connect(**db_config)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
    return None

@app.route('/productos/<int:producto_id>', methods=['GET'])
def get_producto(producto_id):
    connection = create_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos WHERE id = %s", (producto_id,))
        producto = cursor.fetchone()
        cursor.close()
        connection.close()
        if producto:
            return jsonify(producto)
        return jsonify({"error": "Producto no encontrado"}), 404
    return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

# Iniciar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
